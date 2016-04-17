require 'pry'
require 'awesome_print'

# folder = "ecologicalInference_04-04-16_range1.csv/"
# folder = "ecologicalInference_04-04-16_range2.csv/"
folder = "ecologicalInference_04-04-16_all.csv/"

# Wrangles ibge file
ibge_dist = {}
f_ibge = File.open("ibge2010_genero.csv")
f_ibge.each_line do |line|	
	splitted = line.split(";")
	next if splitted[0] == ""	
	ibge_dist[splitted[2]] = {}
	ibge_dist[splitted[2]]["Homem"] = splitted[4].strip
	ibge_dist[splitted[2]]["Mulher"] = splitted[5].strip
end

sent_dist = {}
f_sentiment = File.open("#{folder}sentiment.csv")
f_sentiment.each_line do |line|
		next if line =~/metadata_source_id/ 
		splitted = line.split(",")
		# next if splitted[10] == ""
		negative = splitted[3].to_i
		neutral = splitted[4].to_i
		positive = splitted[5].to_i
		if(sent_dist[splitted[1]] == nil)			
			if positive > negative 
				if(splitted[8] == "1")
					sent_dist[splitted[1]] = {}
					sent_dist[splitted[1]]["positive"] = 1
					sent_dist[splitted[1]]["other"] = 0
					sent_dist[splitted[1]]["homem_positive"] = 1
					sent_dist[splitted[1]]["mulher_positive"] = 0
					sent_dist[splitted[1]]["homem_other"] = 0
					sent_dist[splitted[1]]["mulher_other"] = 0
				elsif(splitted[8] == "2")
					sent_dist[splitted[1]] = {}
					sent_dist[splitted[1]]["positive"] = 1
					sent_dist[splitted[1]]["other"] = 0
					sent_dist[splitted[1]]["homem_positive"] = 0
					sent_dist[splitted[1]]["mulher_positive"] = 1
					sent_dist[splitted[1]]["homem_other"] = 0
					sent_dist[splitted[1]]["mulher_other"] = 0
				end
			else
				if(splitted[8] == "1")
					sent_dist[splitted[1]] = {}
					sent_dist[splitted[1]]["positive"] = 0
					sent_dist[splitted[1]]["other"] = 1			
					sent_dist[splitted[1]]["homem_positive"] = 0
					sent_dist[splitted[1]]["mulher_positive"] = 0
					sent_dist[splitted[1]]["homem_other"] = 1
					sent_dist[splitted[1]]["mulher_other"] = 0
				elsif(splitted[8] == "2")
					sent_dist[splitted[1]] = {}
					sent_dist[splitted[1]]["positive"] = 0
					sent_dist[splitted[1]]["other"] = 1			
					sent_dist[splitted[1]]["homem_positive"] = 0
					sent_dist[splitted[1]]["mulher_positive"] = 0
					sent_dist[splitted[1]]["homem_other"] = 0
					sent_dist[splitted[1]]["mulher_other"] = 1
				end					
			end
		else
			if positive > negative 
				if(splitted[8] == "1")
					sent_dist[splitted[1]]["positive"] += 1
					sent_dist[splitted[1]]["homem_positive"] += 1
				elsif(splitted[8] == "2")
					sent_dist[splitted[1]]["positive"] += 1
					sent_dist[splitted[1]]["mulher_positive"] += 1					
				end
			else
				if(splitted[8] == "1")
					sent_dist[splitted[1]]["other"] += 1		
					sent_dist[splitted[1]]["homem_other"] +=1	
				elsif(splitted[8] == "2")
					sent_dist[splitted[1]]["other"] += 1			
					sent_dist[splitted[1]]["mulher_other"] +=1	
				end				
			end
		end
end

file_ground_truth = File.open("#{folder}ground_truth_genero.csv",'w')

file_ground_truth.write("MUNICIPIO,Y,X,W1,W2,N\n")

sent_dist.keys.each do |municipio|
	next if (sent_dist[municipio]["mulher_positive"].to_f + sent_dist[municipio]["mulher_other"].to_f) == 0
	next if (sent_dist[municipio]["homem_positive"].to_f + sent_dist[municipio]["homem_other"].to_f) == 0
	if(!ibge_dist[municipio].nil?)
		n = sent_dist[municipio]["positive"].to_f + sent_dist[municipio]["other"].to_f		
		percentage_positive  = sent_dist[municipio]["positive"].to_f/(sent_dist[municipio]["positive"].to_f + sent_dist[municipio]["other"].to_f)
		percentage_homem = sent_dist[municipio]["homem_positive"].to_f/ (sent_dist[municipio]["homem_positive"].to_f + sent_dist[municipio]["homem_other"].to_f)
		percentage_mulher = sent_dist[municipio]["mulher_positive"].to_f/ (sent_dist[municipio]["mulher_positive"].to_f + sent_dist[municipio]["mulher_other"].to_f)
		file_ground_truth.write("#{municipio},#{ibge_dist[municipio]["Homem"].to_f * 0.01},#{percentage_positive},#{percentage_homem},#{percentage_mulher},#{n}\n")
	else
		ap("municipio #{municipio} nao encontrado.")
	end
end
f_sentiment.close

# binding.pry
