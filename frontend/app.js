const { createApp } = Vue

createApp({
  data() {
    return {
      file: null,
      prediction: null,
      error: null,
    }
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0];
      this.prediction = null;
      this.error = null;
    },
    async submitFile() {
      if (!this.file) {
        return;
      }

      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const response = await fetch('/predict/', {
          method: 'POST',
          body: formData,
        });

        if (!response.ok) {
          throw new Error('Something went wrong with the prediction.');
        }

        const result = await response.json();

        if (result.error) {
            this.error = result.error;
            this.prediction = null;
        } else {
            this.prediction = result.prediction;
            this.error = null;
        }

      } catch (error) {
        this.error = error.message;
        this.prediction = null;
      }
    }
  }
}).mount('#app')
