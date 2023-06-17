import {api} from '@/plugins/axios'


export default class CompanyService {
    getCompanies(params){
        let url = "/companies/"
        let config = {}
        if (params ) {
            config["params"] = params
        }
        return api.get(url, config)
    }

    search(query){
        let url = "/companies/"
        let config = {params: {search: query}}
        return api.get(url, config)
    }

    getCompany(companyId){
        let url = "/companies/" + companyId + "/"
        return api.get(url)
    }

    createCompany(api, data){
        let url = "/companies/"
        return api.post(url, data)
    }


    patchCompany(companyId, data){
        let url = "/companies/" + companyId + "/"
        return api.patch(url, data)
    }

    getCompanyInformations(companyId){
        let url = "/company-information/"
        let config = {params: {company: companyId}}
        return api.get(url, config)
    }

    createCompanyInformation(data){
        let url = "/company-information/"
        return api.post(url, data)
    }

    getContacts(companyId, params){
        let url = "/companies/" + companyId + "/contacts/"
        let config = {}
        if (params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    createContact(api, companyId, data){
        let url = "/companies/" + companyId + "/contacts/"
        return api.post(url, data)
    }

    deleteContact(api, companyId, contactId){
        let url = "/companies/" + companyId + "/contacts/" + contactId + "/"
        return api.delete(url)
    }
}