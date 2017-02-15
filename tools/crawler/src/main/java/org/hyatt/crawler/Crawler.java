package org.hyatt.crawler;

import java.io.IOException;
import java.net.URI;
import java.net.URISyntaxException;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.ResponseHandler;
import org.apache.http.client.methods.HttpGet;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.apache.http.util.EntityUtils;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.nodes.Element;
import org.jsoup.select.Elements;

public class Crawler {

	private CloseableHttpClient httpclient;
	private String content;
	private Crawler(){
		httpclient = HttpClients.createDefault();
		content = null;
	}
	
	public static Crawler getInstance(){
		return new Crawler();
	}

	public void crawl(String url) throws ClientProtocolException, IOException {
			HttpGet httpget = new HttpGet(url);

//			System.out.println("Executing request " + httpget.getRequestLine());
			// Create a custom response handler
			ResponseHandler<String> responseHandler = new ResponseHandler<String>() {

				public String handleResponse(final HttpResponse response) throws ClientProtocolException, IOException {
					int status = response.getStatusLine().getStatusCode();
					if (status >= 200 && status < 300) {
						HttpEntity entity = response.getEntity();
						if(entity !=null){
							content = EntityUtils.toString(entity);
						}
						EntityUtils.consume(entity);
					} else {
						throw new ClientProtocolException("Unexpected response status: " + status);
					}
					
					return content;
				}

			};
			httpclient.execute(httpget, responseHandler);
	}
	
	public void close() throws IOException{
		httpclient.close();
	}
	

	public String getContent() {
		return this.content;
	}
	
	public static void main(String[] args) {
		Crawler crawler = Crawler.getInstance();
		try {
			String url = "https://www.ncbi.nlm.nih.gov/pmc/?term=hand-arm+bimanual+intensive+therapy%5BAbstract%5D";
			URI uri = new URI(url);
			String host = uri.getHost();
			crawler.crawl(url);
			String content = crawler.getContent();
			Document doc = Jsoup.parse(content);
			Elements eles = doc.select("div.rprt");
			System.out.println("length of eles:"+eles.size());
			for(Element ele:eles){
				System.out.println(host+ele.select("a[href]").first().attr("href"));
			}
		} catch (ClientProtocolException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		} catch (URISyntaxException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

}
