package org.hyatt.crawler;

import java.io.File;
import java.io.IOException;

import org.apache.commons.io.FileUtils;
import org.apache.http.client.ClientProtocolException;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;

public class PUBMEDCrawler {

	private String webEnv;
	private String db;
	private int retstart;
	private int retmax;
	private String base;
	private int totalCount;
	private String queryKey;

	private Crawler crawler;

	public PUBMEDCrawler() {
		base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?";
		webEnv = null;
		db = "pubmed";
		retstart = 0;
		retmax = 10000;
		totalCount = 0;
		this.queryKey = "1";
		crawler = Crawler.getInstance();
	}

	/**
	 * crawl pubmed through e-utilities
	 * 
	 * @throws IOException
	 * @throws ClientProtocolException
	 */
	public void pre_cawl(String query_word) throws ClientProtocolException, IOException {
		// first request get total hits and wenebv
		String url = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=" + db + "&term=" + query_word
				+ "&usehistory=y";
		System.out.println(url);
		crawler.crawl(url);
		Document doc = Jsoup.parse(crawler.getContent());
		String count = doc.select("Count").first().text();
		this.totalCount = Integer.parseInt(count);
		this.webEnv = doc.select("WebEnv").first().text();
		this.queryKey = doc.select("QueryKey").first().text();
		System.out.println("totalCount:" + totalCount);
		System.out.println("WenEnv:" + this.webEnv);
		System.out.println("QueryKey:" + this.queryKey);
	}

	@SuppressWarnings("deprecation")
	public void iter_crawl(String query_word) throws ClientProtocolException, IOException {
		int rounds = totalCount / retmax + 1;
		System.out.println("pages:" + rounds);
		for (int i = 0; i < rounds; i++) {
			retstart = i * retmax;
			System.out.println("crawling page:" + i);
			String url = url_generator(query_word);
			System.out.println(url);
			crawler.crawl(url);
			String content = crawler.getContent();
			File file = new File("habits.txt");
			FileUtils.writeStringToFile(file, content, true);
			try {
				Thread.sleep(2000);
			} catch (InterruptedException e) {
				e.printStackTrace();
			}
		}

	}

	@SuppressWarnings("deprecation")
	public String generate_query(String path) {
		String query_str = "( ";
		try {
			for (String line : FileUtils.readLines(new File(path))) {
				String[] splits = line.split("\t");
				if (splits.length == 3) {
					query_str += splits[1] + "[Title%2FAbstract] OR ";
				}
			}
			query_str = query_str.trim();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		return query_str.substring(0, query_str.length() - 3) + " ) AND Humans[Mesh]";
	}

	public String query_generator(String query_str) {
		query_str = query_str.replace(" ", "+");
		return query_str;
	}

	public String url_generator(String query_word) {
		return base + "db=" + db + "&WebEnv=" + webEnv + "&query_key=" + queryKey + "&retstart=" + retstart + "&retmax="
				+ retmax;
	}

	public static void main(String[] args) {
		PUBMEDCrawler pc = new PUBMEDCrawler();
//		String query_str = pc.generate_query("test-filtered.txt");
		String query_str="hand arm bimanual intensive[Title/Abstract]";
		System.out.println(query_str);
		String query_word = pc.query_generator(query_str);
		try {
			pc.pre_cawl(query_word);
			pc.iter_crawl(query_word);
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

}
