import sentencepiece as spm

def train(input_file,vocab_size,model_name,model_type,character_coverage):
    """
    重要说明（官方参数文档可查）：
    https://github.com/google/sentencepiece/blob/master/doc/options.md

    参数含义：
    - input_file: 原始语料文件路径（每行一句，SentencePiece 会做 Unicode NFKC 规范化）
                  支持多文件逗号拼接：'a.txt,b.txt'
    - vocab_size: 词表大小，如 8000 / 16000 / 32000
    - model_name: 模型前缀名，最终会生成 <model_name>.model 和 <model_name>.vocab
    - model_type: 模型类型：unigram（默认）/ bpe / char / word
                  注意：若使用 word，需要你在外部先分好词（预分词）
    - character_coverage: 覆盖的字符比例
        * 中文/日文等字符集丰富语言建议 0.9995
        * 英文等字符集小的语言建议 1.0
    """

    #这里使用字符串命令式的调用来制定训练参数
    #固定4个特殊发好的id:<pad>=0,<unk>=1,<bos>=2,,<eos>=3
    #这与下游Transformer常用配置一致,便于对齐
    input_argument=(
        '--input=%s '
        '--model_prefix=%s '
        '--vocab_size=%s '
        '--model_type=%s '
        '--character_coverage=%s '
        '--pad_id=0 --unk_id=1 --bos_id=2 --eos_id=3 '
    )
    #将传入参数填充到命令字符串
    cmd=input_argument%(input_file,model_name,vocab_size,model_type,character_coverage)

    #开始训练,会在当前工作目录下生成,<model_name>.model/<model_name>.vocab
    spm.SentencePieceTrainer.Train(cmd)

def run():
    #英文分词器设置
    en_input='../data/corpus.en' # 英文语料：一行一句
    envocab_size=32000# 词表大小：翻译任务常见为 16k/32k
    en_model_name='eng'# 输出前缀：会生成 eng.model / eng.vocab
    en_model_type=('bpe')# 使用 BPE（也可尝试 unigram）
    en_character_coverage=1.0# 英文字符集小 → 用 1.0

    train(en_input,envocab_size,en_model_name,en_model_type,en_character_coverage)

    # ===== 中文分词器配置 =====
    ch_input = '../data/corpus.ch'  # 中文语料：一行一句（无需预分词）
    ch_vocab_size = 32000
    ch_model_name = 'chn'
    ch_model_type = 'bpe'
    ch_character_coverage = 0.9995  # 中文推荐 0.9995，极少数冷僻字会映射为 <unk>

    train(ch_input, ch_vocab_size, ch_model_name, ch_model_type, ch_character_coverage)

def test():
    #加载并调用已经训练好的模型进行编码,解码的示例
    sp=spm.SentencePieceProcessor()
    text="忍耐,就是要想得开,挺得住"

    #加载中文模型(确保chn.model位于当前的工作目录
    sp.Load("./chn.model")

    #编码为子词片段(字符串),如['▁美国', '总统', ...]
    print(sp.EncodeAsPieces(text))

    #编译为id(整数序列)
    print(sp.EncodeAsIds(text))

    #示例:给定一串id ,解码为文本
    a=[28722, 30030, 30164, 28723, 85, 3151, 28805, 28889, 28723, 30471, 19624]
    #注意Python API的方法名是CamelCase:DecodeIds/Decodepieces
    print(sp.DecodeIds(a))

if __name__=="__main__":
    #run()
    test() #训练完后,取消注释进行一次快速功能验证





















