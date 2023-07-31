export default class UserAccountService {
    getAccounts(api, projectId, params){
        let url = "/projects/" + projectId + "/accounts/"
        let config = {}
        if(params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    createAccount(api, projectId, data){
        let url = "/projects/" + projectId + "/accounts/"
        return api.post(url, data)
    }

    deleteAccount(api, projectId, accountId){
        let url = "/projects/" + projectId + "/accounts/" + accountId + "/"
        return api.delete(url)
    }

    patchAccount(api, projectId, accountId, data) {
        let url = "/projects/" + projectId + "/accounts/" + accountId + "/";
        return api.patch(url, data);
    }
}