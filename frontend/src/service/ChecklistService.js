export default class ChecklistService {
    getChecklists(api, params){
        let url = "/checks/checklists/"
        let config = {}
        if (params) {
            config["params"] = params
        }
        return api.get(url, config)
    }

    deleteAssetChecklist(api, projectId, checkId){
        let url = "/projects/" + projectId + "/checklists/" + checkId + "/"
        return api.delete(url)
    }

    createAssetChecklist(api, projectId, data){
        let url = "/projects/" + projectId + "/checklists/"
        return api.post(url, data)
    }

    getAssetChecklists(api, projectId, params){
        let url = "/projects/" + projectId + "/checklists/"
        let config = {}
        if(params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    getAssetCategories(api, projectId, params){
        let url = "/projects/" + projectId + "/checklist-categories/"
        let config = {}
        if(params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    getAssetItems(api, projectId, params){
        let url = "/projects/" + projectId + "/checklist-items/"
        let config = {}
        if(params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    patchAssetItem(api, projectId, itemId, data){
        let url = "/projects/" + projectId + "/checklist-items/" + itemId + "/"
        return api.patch(url, data)
    }
}