import config
import server
import services

if __name__ == '__main__':
    app_config = config.AppConfig.from_yaml_file('config.yaml')
    p_svc = services.PresenceService(app_config)
    phs = services.WebhookHandlerService(app_config, p_svc)
    s = server.create_http_server(phs)
    s.run(host='0.0.0.0')
