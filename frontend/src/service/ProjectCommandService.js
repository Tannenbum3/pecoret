export default class ProjectCommandService {
    getCommands(api, projectId, params) {
        let url = "/projects/" + projectId + "/commands/";
        let config = {};
        if (params) {
            config["params"] = params;
        }
        return api.get(url, config);
    }

    createCommand(api, projectId, data) {
        let url = "/projects/" + projectId + "/commands/";
        return api.post(url, data);
    }

    deleteCommand(api, projectId, id) {
        let url = "/projects/" + projectId + "/commands/" + id + "/";
        return api.delete(url);
    }

    patchCommand(api, projectId, id, data) {
        let url = "/projects/" + projectId + "/commands/" + id + "/";
        return api.patch(url, data);
    }
}
