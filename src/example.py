from lib.RemoteTypograf import RemoteTypograf

rt = RemoteTypograf(attr={"rm_tab": 1})
# rt.htmlEntities()
# rt.br(1)
# rt.p(1)
# rt.nobr(3)
print(
    rt.processText('"Вы все еще кое-как верстаете в "Ворде"? - Тогда мы идем к вам!"')
    )
