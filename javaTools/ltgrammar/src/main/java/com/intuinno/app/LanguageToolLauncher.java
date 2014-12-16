package com.intuinno.app;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.List;

import org.languagetool.JLanguageTool;  
import org.languagetool.rules.Rule;
import org.languagetool.rules.RuleMatch; 
import org.languagetool.language.AmericanEnglish;

import au.com.bytecode.opencsv.CSVReader;

import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVRecord;
                      
public class LanguageToolLauncher {
	JLanguageTool langTool_spell = new JLanguageTool(new AmericanEnglish());
	JLanguageTool langTool_grammar = new JLanguageTool(new AmericanEnglish());
	CSVParser articleReader;
		CSVFormat format = CSVFormat.DEFAULT.withHeader().withDelimiter(',');
			
	BufferedWriter outputFileWriter;
	public LanguageToolLauncher(String filename){
		
		for(Rule rule:langTool_spell.getAllRules()){
			if(!rule.isDictionaryBasedSpellingRule())
				langTool_spell.disableRule(rule.getId());
			else langTool_grammar.disableRule(rule.getId());
		}
		
		
		try{
			langTool_grammar.activateDefaultPatternRules();
			articleReader = new CSVParser(new FileReader(filename),format);
			outputFileWriter = new BufferedWriter(new FileWriter("grammar_feature.csv"));
			outputFileWriter.write("commentID,grammarError,spellingError");
			outputFileWriter.newLine();
			int lineCount = 0;
			
						for (CSVRecord record : articleReader){
								
				System.out.println(lineCount);
				lineCount ++;
				String body = record.get("commentBody");
				
				//body = "I are a boy to takee a bus";
				body = body.replace("<br>", "").replace("<br/>", "");
				List<RuleMatch> matches = langTool_spell.check(body);
//				System.out.println(body);
				int matchSize = matches.size();
				for (RuleMatch match: matches){
					if(body.substring(match.getFromPos(), match.getToPos()).equals("\"")) {
//						System.out.println("[spell_nocount] org: "+body.substring(match.getFromPos(), match.getToPos())+", correct: "+match.getSuggestedReplacements());
						if(matchSize>0) matchSize--;
					}
//					else System.out.println("[spell] org: "+body.substring(match.getFromPos(), match.getToPos())+", correct: "+match.getSuggestedReplacements());
				}
				
				List<RuleMatch> matches_g = langTool_grammar.check(body);
				int matchGSize = matches_g.size();
				for (RuleMatch match: matches_g){		
					if(body.substring(match.getFromPos(), match.getToPos()).equals("\"")) {
//						System.out.println("[grammar_nocount] org: "+match.getMessage() +body.substring(match.getFromPos(), match.getToPos())+", correct: "+match.getSuggestedReplacements());
						if(matchGSize>0) matchGSize--;
					}
//					else System.out.println("[grammar] org: "+match.getMessage() +body.substring(match.getFromPos(), match.getToPos())+", correct: "+match.getSuggestedReplacements());
				}
				String result = record.get("commentID")+","+matchGSize+","+matchSize;
				
//				System.out.println(result);
				outputFileWriter.write(result);
				outputFileWriter.newLine();
			}
			
			outputFileWriter.flush();
		}catch(Exception e){
			e.printStackTrace();
		}
	}
	
	public static void main(String[] args){
		if (0 < args.length) {
			String filename = args[0];

			LanguageToolLauncher ltl = new LanguageToolLauncher(filename);
		} else {

			System.out.println("You should input the comment file name");
		}
	}

}
