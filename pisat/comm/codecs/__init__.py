from pisat.comm.codecs.codec_base import CodecBase, CodecTagBase
from pisat.comm.codecs.codec_tag_num import CodecTagNum, TagCharacterError, TagNotExsistError
from pisat.comm.codecs.codec_flag_tag_num import CodecFlagTagNum
from pisat.comm.codecs.codec_im920 import CodecIm920

# メールサーバー的な扱いにする

# メッセージクラス
# 汎用性の高いインターフェース