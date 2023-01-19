'''
Exemplo de construção do Probability Matching (PM), um produto
criado por Elizabeth ??? (citar autora), que visa substituir
o campo médio de chuva por um campo com valores "mais prováveis"
em função do resultado da média do conjunto de previsão.

A FAZER:
1) construir uma função, que deve
   1.A) receber o conjunto de previsões de chuva (entrada)
   1.B) calcular o campo médio
   1.C) retornar o campo de PM, com as mesmas coordenadas
        espaciais do dado de entrada (saída)
'''
import numpy as np
import xarray as xr

# membros da previsão por conjunto (seriam lidos de arquivos)
chuvaMembro1 = np.array([ [0,0,1],[0,2,9],[0,5,50] ], dtype='float')
chuvaMembro2 = np.array([ [7,21,15],[17,60,20],[12,10,8]], dtype='float')
chuvaMembro3 = np.array([ [0,1,5],[0,5,40],[0,1,7]], dtype='float')

# membros em um DataArray do xarray
chuvaMembros = xr.DataArray([chuvaMembro1,chuvaMembro2,chuvaMembro3],
                            dims=['membro','lat','lon'],
                            name='chuva')
nMembros, nLat, nLon = chuvaMembros.shape

# campo médio
chuvaMedia = chuvaMembros.mean(dim='membro')

print('Média do conjunto de previsões: (ANTES DO PROCESSAMENTO)')
print(chuvaMedia)

# nome das dimensões do campo médio, para ser usado na montagem
# do dicionário usado na localização do dado no xr.DataArray
dimsChuvaMedia = chuvaMedia.dims

# arranjo para pesos do campo médio
pesosCampoMedio = np.empty( chuvaMedia.shape, dtype=int )

# arranjo para resultado final: PM
probMatch = np.empty( chuvaMedia.shape )


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
# a CORRIGIR:
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
   # A FAZER: retirar essa parte para simplificar! Usar NUMPY
   dictPosMaxChuvaMedia = dict( zip(dimsChuvaMedia,posMaxChuvaMedia) )
   #print(dictPosMaxChuvaMedia)

   # atribuindo peso ao arranjo de pesos
   pesosCampoMedio[ posMaxChuvaMedia ] = contaBuscaMax

   # substituindo max encontrado por np.nan para
   # seguir com a procura
   chuvaMedia.loc[ dictPosMaxChuvaMedia ] = -999

   # incrementa o contador
   contaBuscaMax += 1

# vetor com todos os dados de todos os membros do conjunto
# de previsões, em ordem reversa dos seus valores
dadosMembrosDecrescente = np.sort( np.ravel( chuvaMembros ) )[::-1]

# loop para atribuir valores ao arranjo com resultado final
posInicial = 0    # posição inicial do intervalo de valores a ser avaliado
for item in np.arange( 1, chuvaMedia.size+1 ):
   
   # obtendo grupos com nMembros valores do vetor organizado
   # em ordem decrescente e obtendo a mediana desses valores
   novoValorCampo = np.median( dadosMembrosDecrescente[ posInicial : nMembros * item ] )

   # atualizando campo final, com as medianas obtidas acima, de acordo com
   # a posição dos maiores valores no campi médio, armazenados em 'pesosCampoMedio'
   probMatch = np.where( pesosCampoMedio == item, novoValorCampo, probMatch)

   # incrementando posição inicial do intervalo de valores a ser avaliado
   posInicial += nMembros

resultadoPM = xr.DataArray(probMatch,
                           dims=dimsChuvaMedia,
                           coords=chuvaMedia.coords,
                           name='PM_'+chuvaMedia.name)

print('Média do conjunto de previsões: (APÓS PROCESSAMENTO)')
print(chuvaMedia)
print('PM do conjunto de previsões:')
print(probMatch)
print('PM em xr.DataArray:')
print(resultadoPM)
