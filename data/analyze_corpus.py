import os

def analyze_corpus(ch_path,en_path):
    '''分析双语语料库文件的详细信息
    :param ch_path:
    :param en_path:
    :return:
    '''

    #检查文件是否存在
    if not os.path.exists(ch_path):
        print(f"中文文件不存在:{ch_path}")
    if not os.path.exists(en_path):
        print(f"英文文件不存在:{en_path}")
        return

    #获取文件大小
    ch_size=os.path.getsize(ch_path)
    en_size=os.path.getsize(en_path)

    #读取文件内容并统计行数
    with open(ch_path,'r',encoding='utf-8') as f:
        ch_lines=f.readlines()
    with open(en_path,'r',encoding='utf-8') as f:
        en_lines=f.readlines()

    #计算字符数,不包括换行符
    ch_chars=sum(len(line.strip()) for line in ch_lines)
    en_chars=sum(len(line.strip()) for line in en_lines)

    #打印统计信息
    print("=" * 50)
    print("语料库统计信息")
    print("=" * 50)
    print(f'\n中文文件({ch_path}):')
    print(f" 文件大小:{ch_size/1024/1024:.2f} MB")
    print(f" 总行数:{len(ch_lines):,}")
    print(f" 总字符数:{ch_chars:,}")
    print(f" 平均每行字符数:{ch_chars/len(ch_lines):.1f}")

    print(f'\n英文文件({en_path}):')
    print(f" 文件大小:{en_size/1024/1024:.2f} MB")
    print(f" 总行数:{len(en_lines):,}")
    print(f" 总字符数:{en_chars:,}")
    print(f" 平均每行字符数:{en_chars/len(en_lines):.1f}")

    #验证中英文行数是否匹配
    if len(ch_lines)==len(en_lines):
        print("\n行数匹配")
    else:
        print("\n函数不匹配,完几把蛋了")

    print("="*50)

if __name__=="__main__":
    ch_path="corpus.ch"
    en_path="corpus.en"
    analyze_corpus(ch_path,en_path)




