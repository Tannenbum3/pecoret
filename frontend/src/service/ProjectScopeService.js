export default class ProjectScopeService {
    getScopes(api, id, params) {
        let url = "/projects/" + id + "/scopes/";
        let config = {};
        if (params) {
            config["params"] = params;
        }
        return api.get(url, config);
    }

    createScope(api, projectId, data) {
        let url = "/projects/" + projectId + "/scopes/";
        return api.post(url, data);
    }

    deleteScope(api, projectId, scopeId) {
        let url = "/projects/" + projectId + "/scopes/" + scopeId + "/";
        return api.delete(url);
    }
}