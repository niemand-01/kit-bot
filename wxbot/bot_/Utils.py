
import re


def emoji_formatter(st):
    ''' _emoji_deebugger is for bugs about emoji match caused by wechat backstage
    like :face with tears of joy: will be replaced with :cat face with tears of joy:
    '''
    emojiRegex = re.compile(r'<span class="emoji emoji(.{1,10})"></span>')
    def _emoji_debugger(st):
        s = st.replace('<span class="emoji emoji1f450"></span',
            '<span class="emoji emoji1f450"></span>') # fix missing bug
        def __fix_miss_match(m):
            return '<span class="emoji emoji%s"></span>' % ({
                '1f63c': '1f601', '1f639': '1f602', '1f63a': '1f603',
                '1f4ab': '1f616', '1f64d': '1f614', '1f63b': '1f60d',
                '1f63d': '1f618', '1f64e': '1f621', '1f63f': '1f622',
                }.get(m.group(1), m.group(1)))
        return emojiRegex.sub(__fix_miss_match, s)
    def _emoji_formatter(m):
        s = m.group(1)
        if len(s) == 6:
            return ('\\U%s\\U%s'%(s[:2].rjust(8, '0'), s[2:].rjust(8, '0'))
                ).encode('utf8').decode('unicode-escape', 'replace')
        elif len(s) == 10:
            return ('\\U%s\\U%s'%(s[:5].rjust(8, '0'), s[5:].rjust(8, '0'))
                ).encode('utf8').decode('unicode-escape', 'replace')
        else:
            return ('\\U%s'%m.group(1).rjust(8, '0')
                ).encode('utf8').decode('unicode-escape', 'replace')
    st = _emoji_debugger(st)
    st = emojiRegex.sub(_emoji_formatter, st)
    return st

emoji_formatter('<span class="emoji emoji1f602"></span>')
