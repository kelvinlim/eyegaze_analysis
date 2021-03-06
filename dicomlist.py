studyname = 'eyegaze'
srcdir = '/home/oldserver/eyegazetask'
destdir = '/home/share/eyegaze_BIDS'
#container_bids = '/home/share/Containers/tjhendrickson-BIDS_scripts-master-v1.1.simg'
container_bids = '/home/share/Containers/tjhendrickson-BIDS_scripts-master-20180811.simg'
container_mriqc = '/home/share/Containers/poldracklab_mriqc_latest-2018-08-21-a8e3533fc542.simg'
container_citify = '/home/share/Containers/tigrlab_fmriprep_ciftify_1.1.8-2.1.1-2018-11-09-90a855d84d2e.simg'
#container_fmriprep = '/home/share/Containers/fmriprep-1.2.5.simg'
container_fmriprep = '/home/share/Containers/fmriprep_20.1.1.simg'
container_mriqc = '/home/share/Containers/mriqc_0.16.1.simg'

# location for the dcm2niix output
dcm2niix_dir = 'dcm2niix_out'

datasets = [
    ['./EG_ARMS01/DICOM', '800', '1500'],
    ['./EG_ARMS04_FU/DICOM', '801', '1501'],
    ['./EG_ARMS04/DICOM', '801', '1502'],
    ['./EG_ARMS07_FU/DICOM', '803', '1503'],
    ['./EG_ARMS07/DICOM', '803', '1504'],
    ['./EG_ARMS08/DICOM', '805', '1505'],
    ['./EG_ARMS09/DICOM', '806', '1506'],
    ['./EG_ARMS13/DICOM', '807', '1507'],
    ['./EG_ARMS13_FU/DICOM', '807', '1508'],
    ['./EG_ARMS14/DICOM', '809', '1509'],
    ['./EG_NC42/DICOM', '810', '1510'],
    ['./EG_NC42_FU/DICOM', '810', '1511'],
    ['./EG_NC46/DICOM', '812', '1512'],
    ['./EG_NC48_teethbrace/DICOM', '813', '1513'],
    ['./EG_NC49/DICOM', '814', '1514'],
    ['./EG_NC50/DICOM', '815', '1515'],
    ['./EG_NC51/DICOM', '816', '1516'],
    ['./EG_NC52_FU/DICOM', '817', '1517'],
    ['./EG_NC52/DICOM', '817', '1518'],
    ['./EG_NC53_FU/DICOM', '819', '1519'],
    ['./EG_NC53/DICOM', '819', '1520'],
    ['./EG_NC54/DICOM', '821', '1521'],
    ['./EG_NC54_FU/DICOM', '821', '1522'],
    ['./EG_NC59/DICOM', '823', '1523'],
    ['./EG_NC60/DICOM', '824', '1524'],
    ['./EG_NC62/DICOM', '825', '1525'],
    ['./EG_NC63/DICOM', '826', '1526'],
#    ['./EG_PilotPT04/DICOM', '827', '1527'],
    ['./EG_PT13_FU/DICOM', '828', '1528'],
    ['./EG_PT13_Part1/DICOM', '828', '1529'],
    ['./EG_PT13_Part2/DICOM', '828', '1530'],
    ['./EG_PT15_FU/DICOM', '831', '1531'],
    ['./EG_PT22/DICOM', '832', '1532'],
    ['./EG_PT24/DICOM', '833', '1533'],
    ['./EG_PT25/DICOM', '834', '1534'],
    ['./EG_PT33/DICOM', '835', '1535'],
    ['./EG_PT45/DICOM', '836', '1536'],
    ['./EG_PT48/DICOM', '837', '1537'],
    ['./EG_PT49/DICOM', '838', '1538'],
    ['./EG_SB01/DICOM', '839', '1539'],
    ['./EG_SB02/DICOM', '840', '1540'],
    ['./EG_SB03/DICOM', '841', '1541'],
    ['./EG_SB04/DICOM', '842', '1542'],
    ['./EG_SB05/DICOM', '843', '1543'],
    ['./EG_SB10/DICOM', '844', '1544'],
#    ['./MR19273/DICOM', '845', '1545'],
#    ['./MR19414/DICOM', '846', '1546'],
#    ['./MR23105/DICOM', '847', '1547'],
#    ['./NC54_FU_unsuccessful/DICOM', '821', '1548'],
#    ['./Phantom03/DICOM', '849', '1549'],
#    ['./Phantom_01/DICOM', '850', '1550'],
    ['./EG_ARMS08_FU/DICOM', '805', '1551'],
    ['./EG_ARMS20_earring/DICOM', '852', '1552'],
    ['./EG_ARMS23/DICOM', '853', '1553'],
    ['./EG_ARMS24/DICOM', '854', '1554'],
    ['./EG_ARMS25/DICOM', '855', '1555'],
    ['./EG_NC87/DICOM', '856', '1556'],
    ['./EG_NC91/DICOM', '857', '1557'],
    ['./EG_PT51/DICOM', '858', '1558'],
    ['./EG_PT52/DICOM', '859', '1559'],
    ['./EG_PT54/DICOM', '860', '1560'],
    ['./EG_PT56/DICOM', '861', '1561'],
    ['./EG_PT57/DICOM', '862', '1562'],
    ['./EG_PT58_EyeGaze_n_MILOS_Protocols/DICOM', '863', '1563'],
    ['./EG_SB14/DICOM', '864', '1564'],
    ['./EG_SB15/DICOM', '865', '1565'],
# added June 13, 2020
    ['./EG_PT60/DICOM', '866', '1566'],
    ['./EG_PT68/DICOM', '867', '1567'],
    ['./EG_PT69/DICOM', '868', '1568'],
    ['./EG_PT70/DICOM', '869', '1569'],
    ['./EG_PT71/DICOM', '870', '1570'],
    ['./EG_PT72/DICOM', '871', '1571'],
    ['./EG_PT73/DICOM', '872', '1572'],
    ['./EG_PT74/DICOM', '873', '1573'],
    ['./EG_PT75/DICOM', '874', '1574'],
    ['./EG_PT76/DICOM', '875', '1575'],
    ['./EG_PT77/DICOM', '876', '1576'],
    ['./EG_PT78/DICOM', '877', '1577'],
    ['./EG_PT84/DICOM', '878', '1578'],
    ['./EG_ARMS27/DICOM', '879', '1579'],
    ['./EG_ARMS31/DICOM', '880', '1580'],
    ['./EG_ARMS32/DICOM', '881', '1581'],
    ['./EG_ARMS33/DICOM', '882', '1582'],
    ['./EG_ARMS34/DICOM', '883', '1583'],
    ['./EG_ARMS35/DICOM', '884', '1584'],
    ['./EG_ARMS36/DICOM', '885', '1585'],
    ['./EG_ARMS37/DICOM', '886', '1586'],
    ['./EG_ARMS38/DICOM', '887', '1587'],
# error    ['./EG_SB14/DICOM', '888', '1588'],
    ['./EG_SB15/DICOM', '889', '1589'],
    ['./EG_SB17/DICOM', '890', '1590'],
    ['./EG_SB19/DICOM', '891', '1591'],
    ['./EG_SB20/DICOM', '892', '1592'],
    ['./EG_SB21/DICOM', '893', '1593'],
    ['./EG_SB22/DICOM', '894', '1594'],
    ['./EG_SB23/DICOM', '895', '1595'],
    ['./EG_SB24/DICOM', '896', '1596'],
    ['./EG_SB25/DICOM', '897', '1597'],
    ['./EG_SB26/DICOM', '898', '1598'],
    ['./EG_SB27/DICOM', '899', '1599'],
    ['./EG_SB28/DICOM', '900', '1600'],
    ['./EG_SB29/DICOM', '901', '1601'],
    ['./EG_SB31/DICOM', '902', '1602'],
    ['./EG_NC92/DICOM', '903', '1603'],
    ['./EG_NC93/DICOM', '904', '1604'],
    ['./EG_NC98/DICOM', '905', '1605'],
    ['./EG_NC99/DICOM', '906', '1606'],
    ['./EG_NC101/DICOM', '907', '1607'], 
    ['./EG_NC103/DICOM', '908', '1608'], 
    ['./EG_PT80/DICOM', '909', '1609'],  
    ['./EG_ARMS22/DICOM', '910', '1610'],  
    ['./EG_ARMS31_FU/DICOM', '880', '1611'],  
    ['./EG_ARMS32_FU/DICOM', '881', '1612'],  
    ['./EG_ARMS34_FU/DICOM', '883', '1613'],  
    ['./EG_NC59_FU/DICOM', '823', '1614'],  
    ['./EG_NC60_FU/DICOM', '824', '1615'],  
    ['./EG_NC87_FU/DICOM', '856', '1616'],  
    ['./EG_NC88/DICOM', '911', '1617'],  
    ['./EG_NC91_FU/DICOM', '857', '1618'],  
    ['./EG_PT33_FU/DICOM', '835', '1619'],  
    ['./EG_PT48_FU/DICOM', '837', '1620'],  
    ['./EG_PT49_FU/DICOM', '838', '1621'],  
    ['./EG_PT52_FU/DICOM', '859', '1622'],  
    ['./EG_PT56_FU/DICOM', '861', '1623'],  
    ['./EG_PT57_FU/DICOM', '862', '1624'],  
    ['./EG_PT66/DICOM', '912', '1625'],  
    ['./EG_PT69_FU/DICOM', '868', '1626'],  
    ['./EG_PT76_FU/DICOM', '875', '1627'],  
    ['./EG_SB08/DICOM', '913', '1628'],  
  
   
]

    
    
