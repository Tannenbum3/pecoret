import { api } from '@/plugins/axios'


export default class ProjectService {
    getProjects(api, params) {
        let url = "/projects/"
        let config = {}
        if (params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    getProject(projectId){
        let url = "/projects/" + projectId + "/"
        return api.get(url)
    }

    getProjectMembershipMe(projectId){
        let url = "/projects/" + projectId + "/memberships/me"
        return api.get(url)
    }

    getProjectMemberships(api, projectId, params){
        let url = "/projects/" + projectId + "/memberships/"
        let config = {}
        if (params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    createProject(api, data){
        let url = "/projects/"
        return api.post(url, data)
    }

    deleteProject(api, id){
        let url = "/projects/" + id + "/"
        return api.delete(url)
    }

    patchProject(api, projectId, data){
        let url = "/projects/" + projectId + "/"
        return api.patch(url, data)
    }

    getContacts(api, projectId, params){
        let url = "/projects/" + projectId + "/contacts/"
        let config = {}
        if(params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    createContact(api, projectId, data){
        let url = "/projects/" + projectId + "/contacts/"
        return api.post(url, data)
    }

    deleteContact(api, projectId, contactId){
        let url = "/projects/" + projectId + "/contacts/" + contactId + "/"
        return api.delete(url)
    }

    getLanguages(api){
        let url = "/projects/available-languages/"
        return api.get(url)
    }
}
