# Lab 8 - Using ConfigMaps to manage configuration files in containers
In this lab we will use ConfigMap to create configuration data to be injected into containers so we can change comples application configuration without rebuilding container image.

Why is this helpful?
- Any configuration that needs to be changed during deployment to different environments should not be baked into image. You always use THE SAME image in all environments (so what was tested is actually in production).
- So far we have used environmental variables to do so (eg. PostgreSQL connection string), but sometimes applications require complex configuration files (json, ini file, yaml).

In our case we will want to reconfigure NGINX by changing its conf files. Suppose we want to have different configurations in our test and prod environments (eg. more verbose debugging and diagnostic stats page in test, but disabled in produciton for performance reasons). Note our web does not use health probes at the moment. We can point probes to main page, but that would not be efficient (can be too big causing unnecessary overhead) and would confuse our logs and statistics. Let's configure NGINX feature to serve /health for this purpose.

File healthvhost.conf is already available in your base folder. We will now use it to create ConfigMap. This change will probably be for all environments so we can do it in base kustomization.yaml file:

```yaml
configMapGenerator:
- name: healthvhostconf 
  files:
  - healthvhost.conf 
```

Note if this would be environemnt specific you can use the same thing in overlay using the same (create healthvhost.conf file in your test folder and reference in your kustomization.yaml file in test folder).

Check ConfigMap

```bash
# Get ConfigMaps in test namespace
kubectl get configmap -n test

# Get details of your ConfigMap (change name to reflect yours)
kubectl describe configmap -n test healthvhostconf-85gf2b7d84 
```

Let's inject this file into your web Pod. You will add it as additional volumeMount and ConfigMap will behave as Volume like in previous labs. Changes in your web-deployment.yaml file should look like this:

```yaml
        volumeMounts:
          - name: myimages
            mountPath: /opt/bitnami/nginx/html/images
          - name: config-volume
            mountPath: /opt/bitnami/nginx/conf/vhosts/
      volumes:
        - name: myimages
          azureFile:
            secretName: images-secret
            shareName: images
            readOnly: true
        - name: config-volume
          configMap:
            name: healthvhostconf
```

Deploy this change and test whether /health works.

```bash
curl http://test.20.82.220.171.nip.io/health
```

If everything works, configure livenessProbe and readinessProbe in your web-deployment.yaml file to check against /health.

```yaml
        livenessProbe: 
          httpGet:
            path: /health
            port: 8080
        readinessProbe:
          httpGet:
            path: /health
            port: 8080
```

Make sure your application works. In this labs you have seen how ConfigMaps can be used to change complex configuration files without rebuilding container image.