import axios from 'axios';

const API_URL = 'https://resume-analyzer-ja44.onrender.com';

export const api = {
  analyzeResume: async ({ resumeFile, resumeText, jobDescription }) => {
    try {
      const formData = new FormData();
      formData.append('job_description', jobDescription);
      if (resumeFile) {
        formData.append('resume_file', resumeFile);
      } else {
        formData.append('resume_text', resumeText);
      }

      const response = await axios.post(`${API_URL}/api/analyze`, formData);
      return response.data;
    } catch (error) {
      console.error("API Error:", error);
      throw error;
    }
  }
};
