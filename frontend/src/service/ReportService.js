export default class ReportService {
    getReports(api, projectId, params){
        let url = "/projects/" + projectId + "/reports/"
        let config = {}
        if(params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    getReport(api, projectId, reportId){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/"
        return api.get(url)
    }

    getPreviewReportDocument(api, projectId, reportId){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/report-releases/preview_document/"
        return api.get(url)
    }

    createReport(api, projectId, data){
        let url = "/projects/" + projectId + "/reports/"
        return api.post(url, data)
    }

    deleteReport(api, projectId, reportId) {
        let url = "/projects/" + projectId + "/reports/" + reportId + "/";
        return api.delete(url);
    }

    getReportTemplate(api, reportTemplateId){
        let url = "/report-templates/" + reportTemplateId + "/"
        return api.get(url) 
    }

    updateReport(api, projectId, reportId, data){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/"
        return api.patch(url, data)
    }

    getVersionHistoryItems(api, projectId, reportId, params){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/change-histories/"
        let config = {}
        if(params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    createVersionHistory(api, projectId, reportId, data){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/change-histories/"
        return api.post(url, data)
    }

    deleteChangeHistoryItem(api, projectId, reportId, versionId){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/change-histories/" + versionId + "/"
        return api.delete(url)
    }

    getReportDocuments(api, projectId, reportId, params){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/report-releases/"
        let config = {}
        if(params){
            config["params"] = params
        }
        return api.get(url, config)
    }

    deleteReportDocument(api, projectId, reportId, documentId){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/report-releases/" + documentId + "/"
        return api.delete(url)
    }

    createReportDocument(api, projectId, reportId, data){
        let url = "/projects/" + projectId + "/reports/" + reportId + "/report-releases/"
        return api.post(url, data)
    }
}