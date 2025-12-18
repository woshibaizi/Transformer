import json5
import json
import os

if __name__=="__main__":
    # 获取脚本所在目录，确保路径正确
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    files=['train','dev','test']    #define filelist,enclose test ,train,dev(开发)
    ch_path=os.path.join(script_dir, 'corpus.ch')             #chinese file
    en_path=os.path.join(script_dir, 'corpus.en')             #english file
    ch_lines=[]                     #A list for storing Chinese sentences
    en_lines=[]                     #A list for storing English sentences

    for file in files:
        #Load JSON format corpus files,using utf-8 encoding
        json_path = os.path.join(script_dir, 'json', file+'.json')
        corpus=json5.load(open(json_path,'r',encoding='utf-8'))
        for item in corpus:
            en_lines.append(item[0]+'\n')
            ch_lines.append(item[1]+"\n")

    #write Chinese sentences into file
    with open(ch_path,"w",encoding='utf-8') as fch:
        fch.writelines(ch_lines)

    # write English sentences into file
    with open(en_path, "w", encoding='utf-8') as fen:
        fen.writelines(en_lines)

    #output lines of Chinese and English
    #accurate ans:252777
    print("lines of Chinese:",len(ch_lines))
    print("lines of English:",len(en_lines))

    print("Get Corpus!")