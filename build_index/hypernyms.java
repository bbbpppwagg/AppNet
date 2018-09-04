import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;
import java.util.ArrayList;
import java.util.Iterator;
import java.util.List;
import edu.mit.jwi.Dictionary;
import edu.mit.jwi.IDictionary;
import edu.mit.jwi.item.IIndexWord;
import edu.mit.jwi.item.ISynset;
import edu.mit.jwi.item.ISynsetID;
import edu.mit.jwi.item.IWord;
import edu.mit.jwi.item.IWordID;
import edu.mit.jwi.item.POS;
import edu.mit.jwi.item.Pointer;

public class Hypernyms {

	public static void main(String[] args) throws IOException{

		String wnhome = System.getenv("WNHOME"); //获取WordNet根目录环境变量WNHOME
		String path = wnhome + File.separator+ "dict";
		File wnDir=new File(path);
		IDictionary dict=new Dictionary(wnDir);
		dict.open();//打开词典
		ReadFile rf = new ReadFile();
		List<String> res = new ArrayList();
		res = rf.readFileByLines("E:\\OneDrive\\tag.txt");
		String unknownWord = "";
		for (int i = 0; i < res.size(); i++) {
			unknownWord = res.get(i);
			System.out.println("这是第 "+ i + "个单词： " + unknownWord);
//			writeFile("E:\\dd.txt","这是第 " + i + " 个单词");
//			writeFileOne("E:\\hpytest.txt",unknownWord);
//			writeFile("E:\\hpytest2.txt","这是第 " + i + " 个单词;"+unknownWord);
			getHypernyms(dict,unknownWord);//testing
		}
	}

	public static void getHypernyms(IDictionary dict, String unknownWord){
		
		int number;
		
		
		  // 获取指定的synset
		  IIndexWord idxWord = dict.getIndexWord(unknownWord, POS.NOUN);//获取IndexWord
		  if(idxWord != null) {
			  number = idxWord.getWordIDs().size();
//			  System.out.println(number);
			  for (int i = 0; i < number; i++) {
//				  writeFile("E:\\dd.txt","这是第 " + i + " 个义项");
			      IWordID wordID = idxWord.getWordIDs().get(i); //取出第一个词义的词的ID号
			      IWord word = dict.getWord(wordID); //获取词
			      ISynset synset = word.getSynset(); //获取该词所在的Synset

			      // 获取hypernyms
			      List<ISynsetID> hypernyms =synset.getRelatedSynsets(Pointer.HYPERNYM ); // 通过指针类型来获取相关的词集，其中Pointer类型为HYPERNYM

			      List <IWord > words ;
			      for( ISynsetID sid : hypernyms ){
			          words = dict.getSynset(sid).getWords(); // 从synset中获取一个Word的list
//			          System.out.print(sid + "{");
			          for( Iterator<IWord > iw = words.iterator(); iw.hasNext();){
//			             System.out.print(iw.next().getLemma ());
			        	  
//			        	  writeFile("E:\\dd.txt", iw.next().getLemma());
//			        	  writeFile("E:\\word.txt", iw.next().getLemma());
			        	  writeFileOne("E:\\hpytest3.txt",unknownWord+";"+iw.next().getLemma());
			        	  
//			             if(iw. hasNext ()){
//			                 System.out.print(", ");
//			             }
			          }
			          System .out . println ();
			      }
			  }	  
		  }
		  
		  
		  idxWord = dict.getIndexWord(unknownWord, POS.VERB);//获取IndexWord
		  if(idxWord != null) {
			  number = idxWord.getWordIDs().size();
//			  System.out.println(number);
			  for (int i = 0; i < number; i++) {
//				  writeFile("E:\\dd.txt","这是第 " + i + " 个义项");
			      IWordID wordID = idxWord.getWordIDs().get(i); //取出第一个词义的词的ID号
			      IWord word = dict.getWord(wordID); //获取词
			      ISynset synset = word.getSynset(); //获取该词所在的Synset

			      // 获取hypernyms
			      List<ISynsetID> hypernyms =synset.getRelatedSynsets(Pointer.HYPERNYM ); // 通过指针类型来获取相关的词集，其中Pointer类型为HYPERNYM

			      List <IWord > words ;
			      for( ISynsetID sid : hypernyms ){
			          words = dict.getSynset(sid).getWords(); // 从synset中获取一个Word的list
//			          System.out.print(sid + "{");
			          for( Iterator<IWord > iw = words.iterator(); iw.hasNext();){
			        	  
//			        	  writeFile("E:\\dd.txt", iw.next().getLemma());
//			        	  writeFile("E:\\word.txt", iw.next().getLemma());
			        	  writeFileOne("E:\\hpytest3.txt",unknownWord+";"+iw.next().getLemma());
			        	  
//			             System.out.print(iw.next().getLemma ());
//			             if(iw. hasNext ()){
//			                 System.out.print(", ");
//			             }
			          }
			          System .out . println ();
			      }
			  }	  
		  }  
		  
		  
		  
		  idxWord = dict.getIndexWord(unknownWord, POS.ADJECTIVE);//获取IndexWord
		  if(idxWord != null) {
			  number = idxWord.getWordIDs().size();
			  if(number == 0) {
//				  System.out.println(number);
				  for (int i = 0; i < number; i++) {
//					  writeFile("E:\\dd.txt","这是第 " + i + " 个义项");
					  IWordID wordID = idxWord.getWordIDs().get(i); //取出第一个词义的词的ID号
				      IWord word = dict.getWord(wordID); //获取词
				      ISynset synset = word.getSynset(); //获取该词所在的Synset

				      // 获取hypernyms
				      List<ISynsetID> hypernyms =synset.getRelatedSynsets(Pointer.HYPERNYM ); // 通过指针类型来获取相关的词集，其中Pointer类型为HYPERNYM

				      List <IWord > words ;
				      for( ISynsetID sid : hypernyms ){
				          words = dict.getSynset(sid).getWords(); // 从synset中获取一个Word的list
//				          System.out.print(sid + "{");
				          for( Iterator<IWord > iw = words.iterator(); iw.hasNext();){
				        	  
//				        	  writeFile("E:\\dd.txt", iw.next().getLemma());
//				        	  writeFile("E:\\word.txt", iw.next().getLemma());
				        	  writeFileOne("E:\\hpytest3.txt",unknownWord+";"+iw.next().getLemma());
				        	  
//				             System.out.print(iw.next().getLemma ());
//				             if(iw. hasNext ()){
//				                 System.out.print(", ");
//				             }
				          }
				          System .out . println ();
				      }
				  }	
			  }
  
		  }	  
		  
		  
		  idxWord = dict.getIndexWord(unknownWord, POS.ADVERB);//获取IndexWord
		  if(idxWord != null) {
			  number = idxWord.getWordIDs().size();
			  if (number == 0) {
//				  System.out.println(number);
				  for (int i = 0; i < number; i++) {
//					  writeFile("E:\\dd.txt","这是第 " + i + " 个义项");
				      IWordID wordID = idxWord.getWordIDs().get(i); //取出第一个词义的词的ID号
				      IWord word = dict.getWord(wordID); //获取词
				      ISynset synset = word.getSynset(); //获取该词所在的Synset

				      // 获取hypernyms
				      List<ISynsetID> hypernyms =synset.getRelatedSynsets(Pointer.HYPERNYM ); // 通过指针类型来获取相关的词集，其中Pointer类型为HYPERNYM

				      List <IWord > words ;
				      for( ISynsetID sid : hypernyms ){
				          words = dict.getSynset(sid).getWords(); // 从synset中获取一个Word的list
//				          System.out.print(sid + "{");
				          for( Iterator<IWord > iw = words.iterator(); iw.hasNext();){
				        	  
//				        	  writeFile("E:\\dd.txt", iw.next().getLemma());
//				        	  writeFile("E:\\word.txt", iw.next().getLemma());
				        	  writeFileOne("E:\\hpytest3.txt",unknownWord+";"+iw.next().getLemma());
				        	  
//				             System.out.print(iw.next().getLemma ());
//				             if(iw. hasNext ()){
//				                 System.out.print(", ");
//				             }
				          }
				          System .out . println ();
				      }
				  }	
			  }
  
		  }

//		  writeFileTwo("E:\\hpytest.txt");
	}


	public static void writeFile(String file, String content) {
		BufferedWriter out = null;
		try {
			out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file, true)));
			out.write(content+"\r\n");
		}catch(Exception e) {
			e.printStackTrace();
		}finally {
			try {
				out.close();
			}catch(IOException e) {
				e.printStackTrace();
			}
		}
	}
	
	public static void writeFileOne(String file, String content) {
		BufferedWriter out = null;
		try {
			out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file, true)));
			out.write(content+"\r\n");
		}catch(Exception e) {
			e.printStackTrace();
		}finally {
			try {
				out.close();
			}catch(IOException e) {
				e.printStackTrace();
			}
		}
	}

	public static void writeFileTwo(String file) {
		BufferedWriter out = null;
		try {
			out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file, true)));
			out.write("\r\n");
		}catch(Exception e) {
			e.printStackTrace();
		}finally {
			try {
				out.close();
			}catch(IOException e) {
				e.printStackTrace();
			}
		}
	}

}
