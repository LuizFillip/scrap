

import cdsapi

c = cdsapi.Client()

# 1. Variáveis 3D (Temperatura, Vento Zonal, Vento Meridional) nos 130 níveis
c.retrieve('reanalysis-era5-complete', {
    'date'    : '2025-01-01/to/2025-05-01',
    'levelist': '1/to/82',
    'levtype' : 'ml',
    'param'   : '130/131/132',
    'stream'  : 'oper',
    'time'    : '00/06/12/18',
    'type'    : 'an',
    'area'    : '90/-180/-90/180',
    'grid'    : '1.0/1.0',
    'format'  : 'netcdf',
}, 'ERA5_2019_jun_out_uvt.nc')

# # 2. Variável 2D para reconstrução da Pressão (lnsp)
# c.retrieve('reanalysis-era5-complete', {
#     'date'    : '2024-06-01/to/2024-09-30',
#     'levelist': '1',                # Obrigatório fixar no nível 1 para campos 2D em 'ml'
#     'levtype' : 'ml',
#     'param'   : '152',              # 152: Logarithm of surface pressure (lnsp). Alternativa: 134 (sp)
#     'stream'  : 'oper',
#     'time'    : '00/06/12/18',
#     'type'    : 'an',
#     'area'    : '90/-180/-90/180',
#     'grid'    : '1.0/1.0',
#     'format'  : 'netcdf',
# }, 'ERA5_2019_jun_out_lnsp.nc')