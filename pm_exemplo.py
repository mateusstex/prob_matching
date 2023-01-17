import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# membros da previsão por conjunto (seriam lidos de arquivos)
chuva_membro1 = np.array([ [0,0,1],[0,2,9],[0,5,50] ], dtype='float')
chuva_membro2 = np.array([ [7,21,15],[17,60,20],[12,10,8]], dtype='float')
chuva_membro3 = np.array([ [0,1,5],[0,5,40],[0,1,7]], dtype='float')

# membros em um DataArray do xarray
chuva_membros = xr.DataArray([chuva_membro1,chuva_membro2,chuva_membro3],
                            dims=['membro','lat','lon'],
                            name='chuva')

# campo médio (por enquanto soma!)
chuva_media = chuva_membros.sum(dim='membro')

# campo para vetor
busca = 0
#vetor_chuva_media = np.ravel(chuva_media)
peso_maximo = chuva_media.size

# nome das dimensões do campo médio
dimsChuvaMedia = chuva_media.dims

# índice 2D do maior valor do campo médio
# retorna uma tupla com os índices da pos 
posMaxChuvaMedia = np.unravel_index( 
    np.argmax(chuva_media.values, 
    axis=None), 
    chuva_media.shape)

# dicionário com o nome das dimensões do campo
# e as coordenadas do máximo valor
dictPosMaxChuvaMedia = dict( zip(dimsChuvaMedia,posMaxChuvaMedia) )

##### A FAZER:
'''
1) criar DataArray que receberá os pesos, usando a coordenada obtida
2) criar DataArray temp, com cópia dos dados da média, para alterar
   os valores conforme a busca: buscar sempre o máximo valor, substituindo
   o valor encontrado por np.nan para não afetar a busca seguinte
3) atualizar o DataArray temp, colocando o np.nan no lugar do máximo 
   encontrado
4) inserir o peso na respectiva posição do máximo encontrado, no 
   DataArray que receberá os pesos
'''

print(chuva_media.isel(  dictPosMaxChuvaMedia) ) 
exit()
while busca <= chuva_media.size:
    posMaxChuva = np.unravel_index( np.argmax(chuva_media, axis=None), chuva_media.shape)
    




exit()

print(vetor_chuva_media)
print(vetor_rank_chuva_media)
exit()



print(chuva_membros.shape)
print(chuva_membros)
print('******')
print(chuva_media)

print(np.reshape(np.argsort(np.ravel(chuva_media)),(3,3)))
print(chuva_media.argsort())