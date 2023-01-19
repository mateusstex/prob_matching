import xarray as xr
import numpy as np

def probabilityMatching( prevConjuntoChuva: xr.DataArray ):

    # verificando se o dado é do tipo correto
    if not isinstance( prevConjuntoChuva, xr.DataArray ):
        raise TypeError('Tipo do dado deve ser DataArray do xarray')
    
    # dado deve ter 3D: membros do conjunto, latitude e longitude
    # será assumido que a dimensão mais à esquerda se refere
    # às diferentes previsões.
    ndimsPrev = prevConjuntoChuva.ndim
    if ndimsPrev != 3:
        raise NotImplementedError('Dado deve ser 3D.')
    else:
        dimsNomesPrev = prevConjuntoChuva.dims
        formaPrev = prevConjuntoChuva.shape
    
    # campo médio
    chuvaMedia = prevConjuntoChuva.mean( dim=dimsNomesPrev[0] )
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

        # dicionário com o nome das dimensões do campo
        # e as coordenadas do máximo , para ser usado com 
        # .loc, no xarray
        # A FAZER: retirar essa parte para simplificar! Usar NUMPY
        dictPosMaxChuvaMedia = dict( zip(dimsChuvaMedia,posMaxChuvaMedia) )
        
        # atribuindo peso ao arranjo de pesos
        pesosCampoMedio[ posMaxChuvaMedia ] = contaBuscaMax

        # substituindo max encontrado por np.nan para
        # seguir com a procura
        chuvaMedia.loc[ dictPosMaxChuvaMedia ] = -999

        # incrementa o contador
        contaBuscaMax += 1

    # vetor com todos os dados de todos os membros do conjunto
    # de previsões, em ordem reversa dos seus valores
    dadosMembrosDecrescente = np.sort( np.ravel( prevConjuntoChuva ) )[::-1]

    # loop para atribuir valores ao arranjo com resultado final
    posInicial = 0    # posição inicial do intervalo de valores a ser avaliado
    for item in np.arange( 1, chuvaMedia.size+1 ):
   
        # obtendo grupos com nMembros valores do vetor organizado
        # em ordem decrescente e obtendo a mediana desses valores
        novoValorCampo = np.median( 
            dadosMembrosDecrescente[ posInicial : formaPrev[0] * item ] )

        # atualizando campo final, com as medianas obtidas acima, de acordo com
        # a posição dos maiores valores no campi médio, armazenados em 'pesosCampoMedio'
        probMatch = np.where( pesosCampoMedio == item, novoValorCampo, probMatch)

        # incrementando posição inicial do intervalo de valores a ser avaliado
        posInicial += formaPrev[0]

    resultadoPM = xr.DataArray(probMatch,
                           dims=dimsChuvaMedia,
                           coords=chuvaMedia.coords,
                           name='PM_'+chuvaMedia.name)

    return resultadoPM