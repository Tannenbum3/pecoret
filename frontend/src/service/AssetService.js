export default class AssetService {

    getWebApplications(api, projectId, params){
        let url = "/projects/" + projectId + "/web-applications/"
        let config = {}
        if (params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    createWebApplication(api, projectId, data){
        let url = "/projects/" + projectId + "/web-applications/"
        return api.post(url, data)
    }

    deleteWebApplication(api, projectId, assetId){
        let url = "/projects/" + projectId + "/web-applications/" + assetId + "/"
        return api.delete(url)
    }

    getHosts(api, projectId, params){
        let url = "/projects/" + projectId + "/hosts/"
        let config = {}
        if (params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    createHost(api, projectId, data){
        let url = "/projects/" + projectId + "/hosts/"
        return api.post(url, data)
    }

    deleteHost(api, projectId, hostId){
        let url = "/projects/" + projectId + "/hosts/" + hostId + "/"
        return api.delete(url) 
    }

    getServices(api, projectId, params){
        let url = "/projects/" + projectId + "/services/"
        let config = {}
        if (params){
            config["params"] = params
        }
        return api.get(url, config)
    }
}