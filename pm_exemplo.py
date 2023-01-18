import numpy as np
import matplotlib.pyplot as plt
import xarray as xr

# membros da previsão por conjunto (seriam lidos de arquivos)
chuvaMembro1 = np.array([ [0,0,1],[0,2,9],[0,5,50] ], dtype='float')
chuvaMembro2 = np.array([ [7,21,15],[17,60,20],[12,10,8]], dtype='float')
chuvaMembro3 = np.array([ [0,1,5],[0,5,40],[0,1,7]], dtype='float')

# membros em um DataArray do xarray
chuvaMembros = xr.DataArray([chuvaMembro1,chuvaMembro2,chuvaMembro3],
                            dims=['membro','lat','lon'],
                            name='chuva')

# campo médio (por enquanto soma!)
chuvaMedia = chuvaMembros.sum(dim='membro')

# nome das dimensões do campo médio
dimsChuvaMedia = chuvaMedia.dims

# arranjo para pesos do campo médio
pesosCampoMedio = np.empty( chuvaMedia.shape )


# loop que identifica a ordem dos valores no campo médio
# entrada: campo médio, com N valores
# saída: campo com pesos aos valores, sendo 1 para o maior
#        e N para o menor valor.
#
# como funciona:
#    1) busca pela posição do maior valor no dado de entrada
#    2) atribui o peso ao arranjo de saída, na posição obtida
#    3) atribui um valor negativo na entrada, na posição obtida
#
# a corrigir:
#    1) não alterar a entrada!
contaBuscaMax = 1
pesoMaximo = chuvaMedia.size

while contaBuscaMax <= pesoMaximo:
    
   # índice 2D do maior valor do campo médio:
   # np.argmax retorna o índice do maior valor, dos dados
   # organizados num vetor, e unravel_index retorna uma tupla
   # com os índices nD, baseado na forma passada
   posMaxChuvaMedia = np.unravel_index( 
       np.argmax(chuvaMedia.values, axis=None), 
       chuvaMedia.shape)
   #print(posMaxChuvaMedia)

   # dicionário com o nome das dimensões do campo
   # e as coordenadas do máximo , para ser usado com 
   # .loc, no xarray
   dictPosMaxChuvaMedia = dict( zip(dimsChuvaMedia,posMaxChuvaMedia) )
   #print(dictPosMaxChuvaMedia)

   # atribuindo peso ao arranjo de pesos
   pesosCampoMedio[ posMaxChuvaMedia ] = contaBuscaMax

   # substituindo max encontrado por np.nan para
   # seguir com a procura
   chuvaMedia.loc[ dictPosMaxChuvaMedia ] = -999

   # incrementa o contador
   contaBuscaMax += 1

# A FAZER:
#     1) organizar em ordem decrescente os dados dos membros
#     2) separá-los em grupos contendo a mesma quantidade de membros
#     3) atribuir o valor mediano de cada grupo, do maior para o menor,
#        em cada uma das posições identificadas anteriormente.