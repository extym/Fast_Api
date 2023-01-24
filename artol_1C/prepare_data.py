import csv
import random
import string


# wh_ozon = {'casual':[], 'kgt': []}

# wh_ozon = {'casual': ['OWLM200201', 'OWLM200300', 'OWLB191000', 'OWLB191022', 'OWLB191015', 'ИМRUNN50', 'ИМRUNN40', 'OWLM200302', 'OWLM200100', 'OWLM200301', 'OWLM200202', 'OWLT190301/2', 'OWLT190303/2', 'OWLT190402/2', 'OWLT190702/2', 'OWLT200901/2', 'OWLT190901/2', 'OWLB191032', 'OWLB191033', 'OWLB191034', 'OWLB191035', 'OWLB191036', 'OWLB191037', 'OWLB191038', 'OWLB191039', 'OWLB191044', 'OWLB191045', 'OWLB191046', 'ИМALS80', 'OWLT190305'],
#            'kgt': ['OWLT190101', 'OWLT190302', 'OWLT190403S', 'OWLT190304', 'ИМOWLT190901', 'ИМOWLT200901', 'ИМMAL80', 'ИМHELLS65', 'ИМRUNN60', 'ИМVIND80', 'ИМVIND70', 'ИМVIND60', 'ИМVIND50', 'ИМRAG85', 'ИМRAG100', 'ИМNYB80', 'ИМNYB70', 'ИМNYB60', 'ИМMAL100', 'ИМHELLS80', 'ИМHELLS100', 'ИМHELL65', 'ИМHELL120', 'ИМEL75', 'ИМEL55', 'ИМVINDS80', 'OWLM200400', 'OWLM200601', 'OWLM200602', 'OWLM200600', 'OWLM200103', 'OWLM200101', 'OWLM200102', 'OWLM200200', 'OWLM200501', 'OWLM200502', 'OWLM200500', 'OWLT190601', 'OWLT190404', 'OWLT190401', 'ИМOWLT190702', 'ИМOWLT190303', 'ИМOWLT190301', 'ИМVESS75', 'ИМVESS105', 'ИМSS80', 'ИМSS65', 'ИМSS100', 'ИМSJEL80', 'ИМSJEL65', 'ИМSJEL100', 'OWLT190801', 'ИМOWLT190402', 'OWLT190301', 'OWLT190303', 'OWLT190402', 'OWLT190702', 'OWLT200901', 'OWLT190901', 'TOWLT190302', 'OWLT190201']
#            }

# wh_yandex= {'fbs_ctm': ['ИМOWLT190303', 'ИМSS100'],
#             'fbs_express': ['а0026033', 'а0026027', 'а0027471', 'а0027470', 'ИМOWLT190901', 'ИМOWLT200901', 'OWLM200201', 'а0027568', 'ИМMAL80', 'ИМHELLS65', 'OWLB191000', 'OWLB191022', 'OWLB191015', 'ИМRUNN60', 'ИМRUNN50', 'ИМRUNN40', 'ИМVIND80', 'ИМVIND70', 'ИМVIND60', 'ИМVIND50', 'ИМRAG85', 'ИМRAG100', 'ИМNYB80', 'ИМNYB70', 'ИМNYB60', 'ИМMAL100', 'ИМHELLS80', 'ИМHELLS100', 'ИМHELL65', 'ИМHELL120', 'ИМEL75', 'ИМEL55', 'ИМVINDS80', 'OWLM200400', 'OWLM200302', 'OWLM200601', 'OWLM200602', 'OWLM200600', 'OWLM200103', 'OWLM200100', 'OWLM200101', 'OWLM200102', 'OWLM200301', 'OWLM200200', 'OWLM200501', 'OWLM200502', 'OWLM200500', 'OWLM200202', 'OWLT190601', 'OWLT190404', 'OWLT190401', 'ИМOWLT190702', 'ИМOWLT190301', 'ИМVESS75', 'ИМVESS105', 'ИМSS80', 'ИМSS65', 'ИМSJEL80', 'ИМSJEL65', 'ИМSJEL100', 'OWLT190801', 'ИМOWLT190402', 'OWLT190301', 'OWLT190301/2', 'OWLT190303', 'OWLT190303/2', 'OWLT190402', 'OWLT190402/2', 'OWLT190702', 'OWLT190702/2', 'OWLT200901', 'OWLT200901/2', 'OWLT190901', 'OWLT190901/2', 'TOWLT190302', 'OWLB191032', 'OWLB191033', 'OWLB191034', 'OWLB191035', 'OWLB191036', 'OWLB191037', 'OWLB191038', 'OWLB191039', 'OWLB191044', 'OWLB191045', 'OWLB191046', 'OWLT190201'],
#             'dbs_our_delivery': ['all']
#             }

# # create warehouses ozon for product group
# def read_wh():
#     with open('wh.csv', 'r') as file:
#         reader = csv.reader(file, delimiter = ';')
#         for row in reader:
#             if row[3] == 'Обычный' and row[0] not in wh_ozon['casual']:
#                 wh_ozon['casual'].append(row[0])
#             elif row[3] == 'КГТ' and row[0] not in wh_ozon['kgt']:
#                 wh_ozon['kgt'].append(row[0])
#
#         print(len(wh_ozon))
#         print(len(wh_ozon['casual']))
#         print(len(wh_ozon['kgt']))
#         # return wh_ozon
#
#
# read_wh()

# # create warehouses yandex for product group
# def read_wh():
#     with open('wh_yandex.csv', 'r') as file:
#         reader = csv.reader(file, delimiter = ';')
#         for row in reader:
#             if row[3] == 'СТМ' and row[0] not in wh_yandex['fbs_ctm']:
#                 wh_yandex['fbs_ctm'].append(row[0])
#             elif row[3] == 'Экспресс+СТМ' and row[0] not in wh_yandex['fbs_express']:
#                 wh_yandex['fbs_express'].append(row[0])
#
#         print(wh_yandex)
#
#
# read_wh()

##get vendor_vode (SKU), name, barcode from price
# def read_price():
#     with open('./price.csv', 'r') as file:
#         liist = []
#         reader = csv.reader(file, delimiter = ';')
#         for row in reader:
#             proxy = (row[2], row[3], row[4]) #get vendor_vode (SKU), name, barcode
#             liist.append(proxy)
#         # print(proxy)
#         print(len(liist))
#
#     return liist




#
#
# #dict: key = sku, value = min_quantity
# proxy_list = [{'112233': '6'}, {'113355': '6'}, {'123416': '3'}, {'152637': '6'}, {'1592610': '8'}, {'159825': '2'}, {'192837': '6'}, {'1p16A45': '4'}, {'215689': '4'}, {'228228': '2'}, {'270mmgoldvkl': '5'}, {'283746': '6'}, {'342167': '3'}, {'344123': '5'}, {'4358': '2'}, {'4476520': '2'}, {'4569': '15'}, {'467378843': '2'}, {'54456': '2'}, {'5596': '3'}, {'6554655': '15'}, {'734': '2'}, {'74269666': '2'}, {'776553': '2'}, {'78963': '6'}, {'789654': '15'}, {'8520': '2'}, {'852456': '2'}, {'86464': '2'}, {'918273': '5'}, {'963214': '15'}, {'97865': '2'}, {'AL919hdb': '2'}, {'ARTOL12': '2'}, {'ATH805a': '2'}, {'BNCRG59Paika(0530124)': '27'}, {'BNCRG6Nakrutka053023': '15'}, {'BNCRGobjim0530024': '13'}, {'Bagorpojarn': '2'}, {'Batareikaalkalinovaialexmanlr6aa4ht': '4'}, {'Batareikiaaa10ht': '3'}, {'BrelokEM': '8'}, {'Bretelishyia': '2'}, {'DIMK': '2'}, {'DNS1datchikNalichiySeti': '2'}, {'DatchicTempDLYGranitARA': '2'}, {'DelitelTV2podFrazem51000MGC': '5'}, {'DelitelTV4podFrazem51000MGC': '2'}, {'Din6899d': '56'}, {'Din6899d4mm': '50'}, {'Dpm-3': '2'}, {'Dpm301': '2'}, {'Draiver12dc20': '2'}, {'Ds1990A': '18'}, {'Dybeli1118white100sht': '5'}, {'Dybelid10l40yp100htblack': '4'}, {'Dybelid81508whiteyp50': '3'}, {'Dybelixomyt1118black': '5'}, {'Dybelixomyt1925white': '4'}, {'Dybelixomyt510black': '7'}, {'Dybelixomyt510yp100': '7'}, {'E1000r': '3'}, {'ER143353.6vEEMBBatareika': '2'}, {'Es4022': '100'}, {'F0507Grey': '2'}, {'FTP2PR24AWGCAT5e305м': '32'}, {'FTP4PR24AWGCAT5e305мOptimLAN': '21'}, {'FiltrSmennuiA1B1E1K1dlyRPG500502005': '2'}, {'Fotorele6A100vtWhiteIP44': '2'}, {'Fytbolka': '2'}, {'GPBelui': '7'}, {'GPmetall': '7'}, {'Geniusplusikizvehateli': '2'}, {'Gnezdobnc0532034': '22'}, {'Gnezdof054201': '27'}, {'Gnezdof0542016': '56'}, {'Gnezdof0543044': '42'}, {'Gnezdofhtekertv0543034': '50'}, {'Gryntovkadliavlajnpomaxton1l': '5'}, {'Hitrasprediliteliniekhome': '2'}, {'Hnyrevro1111223m': '5'}, {'Hnyrsetevoievro07518111131': '2'}, {'Ho02vxodalexb1': '6'}, {'HomutKkrepleniuT2T3': '11'}, {'HomutNylon2,5x100black': '12'}, {'HomutNylon2,5x200mmBelui0702004': '9'}, {'HomutNylon2.5x200mmBlack0702014': '9'}, {'HomutNylon3.6x300mmBelui070300': '4'}, {'HomutPodVint4.3x200Belui070204': '2'}, {'HomutPodVint4x150Black': '3'}, {'HomutPremium3x200(2.5x200)black': '11'}, {'HomutPremium4x200(3.6x200)Black': '7'}, {'HomutPremium4x250(3.6x250)Black': '5'}, {'HomutSkrepejPistonom2.5x100Black': '7'}, {'Htekerbncgnezdof053201': '11'}, {'IL07BW': '8'}, {'IO102151': '4'}, {'IO102152': '4'}, {'IO10220A2P': '3'}, {'IO10220B2P': '2'}, {'IO10220B2P2': '3'}, {'IO10221': '2'}, {'IO1022600': '2'}, {'IO10240ispA2P2TERRAKTOVUIplastmasRukav': '4'}, {'IO10240ispB2P2BELUIplastRukav': '3'}, {'IO10250ispB2P1BEZRUKAVA': '3'}, {'IO10250ispB2P2KORICHNEVUIplastmRukav': '3'}, {'IO10250ispB2P3MetalRukav': '2'}, {'IO10250ispB2PplastmRukav': '3'}, {'IO10251P': '2'}, {'IO10252': '3'}, {'IO10254': '3'}, {'IO10254Korichnev': '4'}, {'IO1025552HP': '2'}, {'IO102555HP': '2'}, {'IO102555HPTSH': '2'}, {'IO1026Korichnev': '2'}, {'IP212-141': '2'}, {'Io10226isp031Ayks': '2'}, {'Io10240A2P(2)Korich.KabelPlastmRukav': '3'}, {'Io10240A2P(2)PlastmasRukav': '3'}, {'Io10240A2P3MetalRukav': '3'}, {'Io10240ispA3P3metalRukav': '2'}, {'Io10240ispB2MA2M3metalRukav': '2'}, {'Io10240ispB2P2SERUI': '2'}, {'Io10240ispB2P2TerrakotPlastmRukav': '2'}, {'Io10240ispb2pB': '2'}, {'Io10240ispbzp3': '2'}, {'Io102471': '4'}, {'Io10248isp00': '2'}, {'Io10248isp01': '2'}, {'Io10248isp02': '2'}, {'Io1024SMK4': '4'}, {'Io1025': '3'}, {'Io10250': '2'}, {'Io10250ispA2P1BezRukava': '3'}, {'Io10250ispA2P2KorichnevuiPlastmRukav': '3'}, {'Io10250ispA2P2PlastRukav': '3'}, {'Io10250ispA2P3MetalRukav': '3'}, {'Io10254': '6'}, {'Io1026chernui': '2'}, {'Ipd31m': '11'}, {'Izolenta1510': '13'}, {'Izolenta1925white': '8'}, {'Izolentablack1925': '8'}, {'JEKRJ458P8CCAT5e05-1021': '34'}, {'JekTelefon4P4C0510013': '36'}, {'JurnalEkspluataciiSistemProtivopojZashitu48str': '5'}, {'K04kronshtein': '4'}, {'KPSVVngLS1x2x1': '16'}, {'KPSngAFRLS1x2x02kvmmBuhta200m': '15'}, {'KPSngAFRLS1x2x075Buhta200m': '18'}, {'KPSngFRLS1x2x02Buhta200m': '18'}, {'KPSngFRLS1x2x05Buhta200m': '21'}, {'KRTP10': '2'}, {'KTM-Hk': '2'}, {'KabelC2000kPrinteru': '3'}, {'KabelnuiMarkerKlipsa': '2'}, {'KartaPW02(1.6mm)': '25'}, {'KartaPW06(0.8mm)': '13'}, {'KartaSRID10': '33'}, {'Kc2korobkasoed2par': '21'}, {'Kc4': '16'}, {'Kc4m': '16'}, {'Kc5': '12'}, {'Kcpv1005': '30'}, {'Kcpv2004': '17'}, {'Kcpv205': '72'}, {'Kkcp205mmbyxta100m': '25'}, {'Kleshiplitkorez': '2'}, {'Kliyshrw1990/2': '17'}, {'Knopkaexitkashernaia': '2'}, {'Knsispaio1011a': '2'}, {'Kolizokv125': '10'}, {'Kolpashokrj45itkcs411': '34'}, {'Kompproxodrg458p8c030101': '12'}, {'Korobka10010050': '6'}, {'Korobka12010367': '2'}, {'Korobka6440': '46'}, {'Korobka6460': '39'}, {'Korobka808040': '7'}, {'Korobkatysod70h40': '42'}, {'Korobkatysoraspd100h40': '28'}, {'Korobspaceokub': '2'}, {'Korpysarmstrong': '2'}, {'Kpcngafrls12075byxta200mpylis': '20'}, {'Kpcngafrls1275byxta200mrexant': '25'}, {'Kpsngafrls12075200': '15'}, {'Kpsngafrls2215byxta200msi': '9'}, {'Krepejkabeliakrugl1250': '14'}, {'Krepejkabeliakrygl950': '10'}, {'Kreplenieh3': '23'}, {'Krepleniet3oy3op4srezinkoi': '2'}, {'Krepleniet4dliaoy3op4': '2'}, {'Kreplenietv4': '2'}, {'Kreplenietv8': '2'}, {'Kristal12V': '2'}, {'Kronhteinkastre5': '10'}, {'Kronhteinkastre5harik': '9'}, {'Lompojarn': '3'}, {'Lopatapojsovkov': '2'}, {'Mayk123M': '2'}, {'Mkvideo': '3'}, {'Modyli5684': '8'}, {'Moiniy12VOSNOVA': '2'}, {'Moiniy243OSNOVA': '2'}, {'Moiniy24Vvuhod': '2'}, {'MoiniyNadpisAvtomatOtkluch': '5'}, {'MolmiyNadpPoroshokUhodi': '5'}, {'Molniy12BPoroshokNeVhody': '2'}, {'Molniy12VPojar': '2'}, {'Molniy12Vvuhod': '2'}, {'Molniy24VGazNeVhodi': '2'}, {'Molniy24VGazUhodi': '2'}, {'Molniy24VOsnova': '2'}, {'MolniyNadpGAZNEVHODI': '5'}, {'MolniyNadpGAZUHODI': '5'}, {'MolniyNadpNeVhodit': '5'}, {'MolniyNadpPOJAR': '5'}, {'MolniyNadpPoroshokNevhodi': '5'}, {'MolniyNadpStrelkaVlevo': '5'}, {'MolniyNadpVUHOD': '5'}, {'MolniyNadpZapasnoiVuhod': '5'}, {'Naborklhex15109': '3'}, {'Nakleikanapropysk': '6'}, {'Nakoneshnik575': '6'}, {'Noj565': '3'}, {'OOOPz-24': '3'}, {'Obezjirivateliynevers1l': '3'}, {'OchistitelMontajPenuOppaCleaner05L': '2'}, {'Opop18': '2'}, {'P10': '2'}, {'PDA3-45N100': '2'}, {'PastaGOIdlyPlastika': '5'}, {'Patshkordgrey05': '12'}, {'Penal': '2'}, {'Perecodbncrca0532024': '25'}, {'Perexodnikgnezdof03044': '27'}, {'Petplusikizvehateli': '2'}, {'Pkimb779': '2'}, {'Plakatktiz2l': '5'}, {'Plakatpodeistviampersonalashool': '8'}, {'Plombaplastikgreen': '50'}, {'Plombaplastikovaiayelloy': '50'}, {'Plombaplastikred': '50'}, {'Plombarotornaiawait': '42'}, {'Ploshadka2020072021': '2'}, {'Ploshadka2525072025': '5'}, {'Povorot6060': '4'}, {'Povorot90': '17'}, {'Povorot90d20': '14'}, {'Pp-600': '2'}, {'RCA14-0403': '33'}, {'RCA14-0409-4': '19'}, {'REXANT05-3076': '12'}, {'RVI/Whi/Bla/Pla': '9'}, {'Rastrybkoy1': '16'}, {'Rastrybkoy234': '12'}, {'RaxemFrazemRG6(054003)': '50'}, {'RazemFrazemRG59(0540024)': '55'}, {'RazemGnezdoBNCsKlemmnoiKolodkoi(053081)': '8'}, {'RazemPitaniy2.1x5,5x10mmSprovodom20sm(140313)': '23'}, {'RazemPitaniyShtekerSklemnoiKolodkoi(140314)': '13'}, {'RazemShtekerPodVintSprujinoiMetall(053073)': '17'}, {'Razempitaniia1403141': '8'}, {'RazvetvitelPitaniyNa9razemov(140317)': '2'}, {'Registor470kom': '84'}, {'Rexant140413': '12'}, {'Rezistor523om': '100'}, {'Rezistormlt0125': '84'}, {'Rfidemrw': '10'}, {'RoxetkaNakladnayReoneSzazemlBelay': '7'}, {'RozetkaDvoinayNakladSCHNEIDERELECTRICZazeml': '2'}, {'RozetkaKomputernay1RJ45CAT5e030121': '4'}, {'RozetkaKomputernay2RJCAT5e030151': '3'}, {'RozetkaTelefonnayNakladnay26P4C2Porta030008': '4'}, {'RozetkaTelefonnayUniversalnayBelay030011': '17'}, {'RozetkaTelefonnayVnutrennyy26P4C2porta030010': '4'}, {'RukavUVP1Vnutrikv19mmVSumkeStvolShtutcerRukavPVH': '2'}, {'RuletkaProfi3m16mmProrezinennuiKorpus129004': '4'}, {'RuletkaProfi5m25mmProrezinennuiKorpus129006': '2'}, {'SchituvatelCDTM01': '2'}, {'ShetkapometallyVertextools245': '4'}, {'Shtekerrcapodpaiky': '26'}, {'Shvvp2075200m': '20'}, {'SkobaD19SMDdvuhlapkovay': '100'}, {'SkotchLokIzolirovannuiK2': '84'}, {'SkotchLokKZ075403': '50'}, {'Skrebokdliakraski': '2'}, {'SoedinitelnayPlastinaDKS': '7'}, {'Spbox12050indor': '3'}, {'Srid30': '13'}, {'StEX011sm': '11'}, {'Stoikaosnovaniedliasistemvravnivaniialitokollit50': '2'}, {'StvolPojPC50A': '2'}, {'TalrepKrukKolco095648': '3'}, {'TarelkaOpornayDlyUSHMiDreliVira150mm': '2'}, {'Trybki2': '7'}, {'Trybki3': '9'}, {'Trybki5': '6'}, {'Trybki6': '7'}, {'UTP4PR24AWGCAT5e305мVnutrenniiOptimLAN': '20'}, {'Utp101phd6': '2'}, {'VedroPojarnoeKonusnoe': '2'}, {'Vertlug4.5mm': '11'}, {'Vilka030012': '19'}, {'Vilkabezzazemleniiawhite': '5'}, {'Vintsamorez2916': '6'}, {'Vvgngls315100': '8'}, {'Ydlinitelibtovoilexman3zazemleniia': '2'}, {'ZagimDUPLEX2mmOCdlytrosa': '30'}, {'ZajimDlyTrosa34mm095603': '32'}, {'Zamoknavesnoistanders3127mm': '3'}, {'Zamoknavesnoistanders4033mm': '2'}, {'Ziklop4654': '2'}, {'Znakaptechka100100': '17'}, {'ZubrDupelStandartsShurup6x40': '100'}, {'artoladsl': '3'}, {'artolart0230': '13'}, {'artolart10': '12'}, {'artolart555': '10'}, {'artolart7': '3'}, {'artolastra': '2'}, {'artolastram2': '2'}, {'artolblack': '2'}, {'dg56fhu8gj90': '7'}, {'dg7fuv84ch32': '9'}, {'dgc45dghv7of98': '5'}, {'dgcc565rugf785': '5'}, {'dst200s36': '5'}, {'homutNylon2.5x100mm100shtBelui': '17'}, {'ip212-69/3M': '2'}, {'ip2123CY': '4'}, {'izveshateli103-4/1': '4'}, {'izveshateli105-1-50': '2'}, {'izveshateli114-50-A3': '5'}, {'izveshateli5-01T': '2'}, {'izveshateli6973': '2'}, {'jgv4hib78iu': '8'}, {'jh67fujc98gjv4': '8'}, {'jh6dhv34oh09': '8'}, {'knopkaexitb': '2'}, {'lki7gh9fuc34dg': '8'}, {'nabortermoycadosh5664': '11'}, {'napravliaishaiastrelka987456': '6'}, {'nosmoking459023': '10'}, {'ognetyshuteli451098': '12'}, {'ognetyshznak452178': '10'}, {'opasnostitok902156': '10'}, {'opasnostitokfotolym9836': '10'}, {'otvetstvenbezopasnosti3081': '10'}, {'podgarnoesostoianie2047': '10'}, {'pojarngidrant4950': '10'}, {'pojarnkran96367': '10'}, {'pojarnshit4702': '8'}, {'pojarnsyhotrybn6874': '5'}, {'pojarznal76840': '10'}, {'postoronzapret': '13'}, {'ppodgarnaialestniza1058': '10'}, {'pripojarezvoniti101112': '10'}, {'sf7fug46fi07': '2'}, {'shipznak5741': '4'}, {'stoinapriajenie85770': '10'}, {'vedetsyvideonabl150200': '13'}, {'vg4tgu82ffg61': '7'}, {'vhod1500300': '5'}, {'vhodzapreshen7487': '10'}, {'vodoistoshnik3801': '10'}, {'vuhodLevo': '5'}, {'vuhodpravo200200': '5'}, {'ykazatelinapriajeniia57420': '14'}, {'ykazatelivxod85860': '10'}, {'zapasnoiavxod46860': '10'}, {'zapretkuren220': '13'}, {'zapretkurit200200': '13'}, {'zazemleno50100': '20'}, {'znakaptechka200': '13'}, {'znakognet872018': '10'}, {'znakpesok1092': '10'}, {'zvonitipripojsre36447': '10'}, {'ИПР-55К': '2'}, {'ио102161': '5'}]
#
# ##get minquantity from price list
# def read_shop_feed():
#     with open('./price_2023.csv', 'r') as file:
#         dicty = {}
#         reader = csv.reader(file, delimiter = ';')
#         count = 0
#         for row in reader:
#
#             proxy = {}
#             if row[3] is not None and row[9].isdigit():
#                 # proxy[row[2]] = row[9]
#                 dicty[row[2]] = row[9]
#                 count += 1
#
#         # liist = liist[3:]
#         count -= 3
#         print(count, dicty)
#
# read_shop_feed()


##create dict from price and response 1C - concat id_ic & other data from price
# def create_target_data():
#     target = {}
#     complete_data = read_price()  #get id_ic, vendor_vode (SKU), name, barcode from price_list.csv
#     for key, value in data.items():
#         for row in complete_data:
#             if value[0] == row[0] and value[0] != '':
#                 target[key] = row
#                 #print(target[key])
#
#     with open('target.json', 'w') as file:
#         json.dump(target, file)
#
#     #print(target)
#     print('target len  -', len(target))
#     return target


#get Ozon_proguct_id
# def get_proxy_data():
#     with open('current.csv', 'r') as file:
#         reader = csv.reader(file, delimiter=';')
#         proxy = []
#         faxy = []
#         for row in reader:
#             proxy.append(row)
#             faxy.append(row[2])
#
#     del proxy[0]
#     del faxy[0]
#
#     print(*faxy, sep='", "')
#
#     return proxy
#
# #data = get_proxy_data()


# def get_ozon_sku():
#     datas = read_file()   # data from json
#     proxy =  get_proxy_data()  #data from csv
#     l = [proxy[i][1] for i in range(len(proxy))]  #list product_id from csv
#     for i in range(len(datas)):
#         product_id = str(datas[i]['product_id'])
#         index = l.index(product_id)
#         offer_id = proxy[index][0]
#         #print(type(product_id), type(proxy[index][1]))
#         if product_id == proxy[index][1]:
#             datas[i]['offer_id'] = offer_id
#     #print(datas[2])
#     write_file(datas)
#
# #get_ozon_sku()

# from datetime import datetime, timezone
# from backports.zoneinfo import ZoneInfo
# dt = datetime.now()
# dt = dt.replace(tzinfo=ZoneInfo('Africa/Nairobi')).isoformat()
# print(dt)
# # print(dt.isoformat())
#
# import pytz
from datetime import datetime, timedelta
#
# time = datetime.now(pytz.timezone("Africa/Nairobi")).replace(microsecond=0).isoformat()
# print(time)


# from datetime import date, datetime, time, timedelta
#
# dt = datetime.now().date() + timedelta(days=2)
# d = str(dt).split('-')
# d.reverse()
# pt = '-'.join(d)
# print(pt)



# def token_generator(size=24, chars = string.ascii_lowercase + string.digits):
#     return ''.join(random.choice(chars) for _ in range(size))
#
# print(token_generator())


# def token_generator(size=24, chars = string.ascii_lowercase + string.digits):
#     result = ''.join(random.choice(chars) for _ in range(size))
#     return result
#     print('111', result)
# print(token_generator())