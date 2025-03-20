async function analyzeText() {
    const text = document.getElementById("textInput").value;
    if (!text) return alert("Please enter text to analyze.");

    const response = await fetch("/predict-text", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text }),
    });

    const data = await response.json();
    document.getElementById("result").innerText = `🎭 Sentiment: ${data.sentiment}`;
}

async function analyzeImage() {
    const fileInput = document.getElementById("imageInput");
    const file = fileInput.files[0];
    if (!file) return alert("Please select an image file.");

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/predict-image", { method: "POST", body: formData });
    const data = await response.json();

    if (data.error) {
        document.getElementById("result").innerText = `⚠️ Error: ${data.error}`;
    } else {
        document.getElementById("result").innerText = `🎭 Sentiment: ${data.sentiment}\n📝 Extracted Text: ${data.extracted_text}`;
    }
}

async function analyzeImageUrl() {
    const url = document.getElementById("imageUrl").value;
    if (!url) return alert("Please enter an image URL.");

    const response = await fetch("/predict-url", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url }),
    });

    const data = await response.json();
    
    if (data.error) {
        document.getElementById("result").innerText = `⚠️ Error: ${data.error}`;
    } else {
        document.getElementById("result").innerText = `🎭 Sentiment: ${data.sentiment}\n📝 Extracted Text: ${data.extracted_text}`;
    }
}
