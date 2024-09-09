Desde srv.py:
  rec para grabar
  play para reproducir
  stop para detener tanto la grabacion como la reproducion
  send recolecta los audios de todos los clientes conectados
  close cierra conexion con los clientes y detiene los bucles 

Para conpilar en Android:
  
  Descomentar en main.py
    
    #from android.permissions import request_permissions, Permission
    
    #request_permissions([Permission.RECORD_AUDIO, Permission.WAKE_LOCK, Permission.READ_EXTERNAL_STORAGE, Permission.WRITE_EXTERNAL_STORAGE, Permission.INTERNET])

  Modificar AndroidManifest.xml agregando: 
  
  <application 
      #
      #
      android:requestLegacyExternalStorage="true">  

  
