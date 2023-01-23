import xarray as xr
import numpy as np
from pm_funcao import probabilityMatching

# membros da previsão por conjunto (seriam lidos de arquivos)
chuvaMembro1 = np.array([ [0,0,1],[0,2,9],[0,5,50] ], dtype='float')
chuvaMembro2 = np.array([ [7,21,15],[17,60,20],[12,10,8]], dtype='float')
chuvaMembro3 = np.array([ [0,1,5],[0,5,40],[0,1,7]], dtype='float')

# membros em um DataArray do xarray (testando git no windows)
chuvaMembros = xr.DataArray([chuvaMembro1,chuvaMembro2,chuvaMembro3],
                            dims=['membro','lat','lon'],
                            name='chuva')



print( chuvaMembros.shape )
print( chuvaMembros.dims)

teste = probabilityMatching( chuvaMembros )
print(teste)
print(chuvaMembros.mean(dim='membro'))


