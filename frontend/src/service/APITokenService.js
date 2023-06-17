export default class APITokenService {
    getTokens(api, projectId, params){
        let url = "/projects/" + projectId + "/api-tokens/"
        let config = {}
        if (params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    deleteToken(api, projectId, tokenId){
        let url = "/projects/" + projectId + "/api-tokens/" + tokenId + "/"
        return api.delete(url, {})
    }

    createToken(api, projectId, data){
        let url = "/projects/" + projectId + "/api-tokens/"
        return api.post(url, data)
    }
}