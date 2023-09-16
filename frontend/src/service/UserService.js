export default class UserService {
    getAPITokens(api, params) {
        let url = "/api-tokens/";
        let config = {};
        if (params) {
            config["params"] = params;
        }
        return api.get(url, config);
    }

    deleteAPIToken(api, id) {
        let url = "/api-tokens/" + id + "/";
        return api.delete(url);
    }

    createAPIToken(api, data) {
        let url = "/api-tokens/";
        return api.post(url, data);
    }

}