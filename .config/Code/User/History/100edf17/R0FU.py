import csv

with open('municipios.csv', 'r', encoding='utf-8') as t1, open('res.state.city.csv', 'r', encoding='utf-8') as t2:
    mds_csv = csv.reader(t1)
    # next(mds_csv)
    # mds_csv = t1.readlines()

    ibge_csv = csv.reader(t2)
    next(ibge_csv)
    # ibge_csv = t2.readlines()

    for linha in ibge_csv:

        # print(type(linha[5]))

        for linha_mds in mds_csv:
            # if linha[5] == linha_mds[1].strip():
            
            print(f'{linha_mds[1]}')
            # print(linha_mds[1].rstrip())


# with open('res.state.city.csv', 'r', encoding='utf-8') as t2:
#     new_csv = csv.reader(t2)
#     next(new_csv)

# with open('update.csv', 'w', encoding='utf-8') as out_file:
#     # line_in_new = 0
#     # line_in_old = 0

#     leitor_csv = csv.reader(out_file)
#     mds_csv = csv.reader
#     # leitor_csv.next()



#     for linha in ibge_csv[1:]:

#         # print(linha)

#         for linha_mds in mds_csv:

#             if linha[5] == linha_mds[1]:
#                 print(linha, linha_mds[1])
#                 # linha.append(linha)
#                 # linha.appned(linha_mds[0])


    # while line_in_new < len(new_csv) and line_in_old < len(old_csv):

    #     if old_csv[]



    #     if old_csv[line_in_old] != new_csv[line_in_new]:
    #         out_file.write(new_csv[line_in_new])
    #     else:
    #         line_in_old += 1
    #     line_in_new += 1