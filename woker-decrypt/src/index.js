/**
 * Welcome to Cloudflare Workers! This is your first worker.
 *
 * - Run `npm run dev` in your terminal to start a development server
 * - Open a browser tab at http://localhost:8787/ to see your worker in action
 * - Run `npm run deploy` to publish your worker
 *
 * Learn more at https://developers.cloudflare.com/workers/
 */

import MixBase64 from './mixBase64';
import AesCTR from './aesCTR';


export default {
	async fetch(request, env, ctx) {

		    //请求头部、返回对象
			let reqHeaders = new Headers(request.headers),
			outBody, outStatus = 200, outStatusText = 'OK', outCt = null, outHeaders = new Headers({
				"Access-Control-Allow-Origin": reqHeaders.get('Origin'),
				"Access-Control-Allow-Methods": "GET, POST, PUT, PATCH, DELETE, OPTIONS",
				"Access-Control-Allow-Headers": reqHeaders.get('Access-Control-Allow-Headers') || "Accept, Authorization, Cache-Control, Content-Type, DNT, If-Modified-Since, Keep-Alive, Origin, User-Agent, X-Requested-With, Token, x-access-token, Notion-Version"
			});

			const range = request.headers.range
			const start = range ? range.replace('bytes=', '').split('-')[0] * 1 : 0
		
		
			try {
				//取域名第一个斜杠后的所有信息为代理链接
				let url = request.url.substr(8);
				url = decodeURIComponent(url.substr(url.indexOf('/') + 1));
		  
				//需要忽略的代理
				if (request.method == "OPTIONS" && reqHeaders.has('access-control-request-headers')) {
					//输出提示
					return new Response(null, PREFLIGHT_INIT)
				}
				else if(url.length < 3 || url.indexOf('.') == -1 || url == "favicon.ico" || url == "robots.txt") {
					return Response.redirect('https://baidu.com', 301)
				}
				//阻断
				else if (blocker.check(url)) {
					return Response.redirect('https://baidu.com', 301)
				}
				else {
					//补上前缀 http://
					url = url.replace(/https:(\/)*/,'https://').replace(/http:(\/)*/, 'http://')
					if (url.indexOf("://") == -1) {
						url = "http://" + url;
					}
					//构建 fetch 参数
					let fp = {
						method: request.method,
						headers: {}
					}
					//保留头部其它信息
					let he = reqHeaders.entries();
					const requrl = new URL(url);

					const password = requrl.searchParams.get("enc_password");
					const filesize = requrl.searchParams.get("enc_filesize");
		
					// if(requrl.hostname.includes('.xunleix.com')){
					//     for (let h of he) {
					//         if (!['content-length', 'cf-ipcountry', 'x-real-ip', 'cf-connecting-ip', 'server'].includes(h[0])) {
					//             fp.headers[h[0]] = h[1]; // 其他头部正常添加
					//         }
					//     }
					//     fp.headers["User-Agent"] = 'AndroidDownloadManager/12 (Linux; U; Android 12; M2004J7AC Build/SP1A.210812.016)'; 
					// }else{
					//     for (let h of he) {
					//         if (!['content-length'].includes(h[0])) {
					//             fp.headers[h[0]] = h[1];
					//         }
					//     }
					// }
		
					if(requrl.hostname=='api-pan.xunleix.com'){
						for (let h of he) {
							if (!['content-length', 'cf-ipcountry', 'x-real-ip', 'cf-connecting-ip', 'server'].includes(h[0])) {
								fp.headers[h[0]] = h[1]; // 其他头部正常添加
							}
						}
					}else{
						for (let h of he) {
							if (!['content-length'].includes(h[0])) {
								fp.headers[h[0]] = h[1];
							}
						}
					}
		
					// 是否带 body
					if (["POST", "PUT", "PATCH", "DELETE"].indexOf(request.method) >= 0) {
						const ct = (reqHeaders.get('content-type') || "").toLowerCase();
						if (ct.includes('application/json')) {
							  let requestJSON = await request.json()
							  console.log(typeof requestJSON)
							fp.body = JSON.stringify(requestJSON);
						} else if (ct.includes('application/text') || ct.includes('text/html')) {
							fp.body = await request.text();
						} else if (ct.includes('form')) {
							fp.body = await request.formData();
						} else {
							fp.body = await request.blob();
						}
					}
					// 发起 fetch
					let fr = (await fetch(new URL(url), fp));
					outCt = fr.headers.get('content-type');
					if(outCt && (outCt.includes('application/text') || outCt.includes('text/html'))) {
					  try {
						// 添加base
						let newFr = new HTMLRewriter()
						.on("head", {
						  element(element) {
							element.prepend(`<base href="${url}" />`, {
							  html: true
							})
						  },
						})
						.transform(fr)
						fr = newFr
					  } catch(e) {
					  }
					}
		
					for (const [key, value] of fr.headers.entries()) {
					  outHeaders.set(key, value);
					}
		
					outStatus = fr.status;
					outStatusText = fr.statusText;

					console.log(filesize);

					var decoder = new AesCTR(password, filesize);
					if(start>0){
						decoder.setPositionAsync(start);
					}
					outBody = decoder.decrypt(fr.body);

				}
			} catch (err) {
				outCt = "application/json";
				outBody = JSON.stringify({
					code: -1,
					msg: JSON.stringify(err.stack) || err
				});
			}
		  
			//设置类型
			if (outCt && outCt != "") {
				outHeaders.set("content-type", outCt);
			}
		  
			let response = new Response(outBody, {
				status: outStatus,
				statusText: outStatusText,
				headers: outHeaders
			})
		  
			return response;





		return new Response('Hello World!');
	},
};
