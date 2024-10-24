#Instructions pour le lot4 

1) Edit avec votres infos locales et  run du script elastic_indexeraser.py dans le package elastic_index_management
```pycon
ES_HOST = 'http://localhost:9200'
INDEX_NAME = 'dataw_fro03'  # Index name to be deleted
ES_USER = 'elastic'
ES_PASSWORD = 'yourpasword' #replace by password
```

2) Edit avec votre config locale et Run du script elasticmappingput.py dans le package elastic_index_management
```pycon
ES_HOST = 'http://localhost:9200'
INDEX_NAME = 'dataw_fro03'  # Index name to be deleted
ES_USER = 'elastic'
ES_PASSWORD = 'yourpasword' #replace by password
```
3) Run Script hbaseverelastic 

4) utilisez kibana au plaisir ou bine utilises les scripts fournis das le package  lot1_Visualisation_dashboar et  lot2_visualisation_dashboard
