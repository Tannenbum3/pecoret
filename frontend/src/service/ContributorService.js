export default class ContributorService {
    getContributors(api, projectId, params){
        let url = "/projects/" + projectId + "/memberships/"
        let config = {}
        if (params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    createContributor(api, projectId, data){
        let url = "/projects/" + projectId + "/memberships/"
        return api.post(url, data)
    }

    deleteContributor(api, projectId, contributorId){
        let url = "/projects/" + projectId + "/memberships/" + contributorId + "/"
        return api.delete(url, {})
    }
}
