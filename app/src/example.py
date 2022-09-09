""" Example for Typograf """
from lib.typograf import Typograf

rt = Typograf(attr={"rm_tab": 1})
# rt.htmlEntities()
# rt.br(1)
# rt.p(1)
# rt.nobr(3)
print(
    rt.processtext('"Вы все еще кое-как верстаете в "Ворде"? - Тогда мы идем к вам!"')
    )
