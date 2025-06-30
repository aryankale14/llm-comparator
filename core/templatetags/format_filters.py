from django import template
import re

register = template.Library()

@register.filter
def format_comparison(value):
    if not value:
        return ""

    # Try to extract the best response (e.g., "Response 3")
    best_match = re.search(r"\*\*Best.*?:\*\*\s*(Response \d)", value)
    best_response = best_match.group(1).strip() if best_match else "Not found"

    # Map response number to model names
    response_map = {
        "Response 1": "GPT-4o-mini",
        "Response 2": "Gemini 2.5",
        "Response 3": "Mistral 12B",
        "Response 4": "LLaMA 3"
    }
    best_label = response_map.get(best_response, best_response)

    # Extract each response block
    response_blocks = re.findall(
        r"\*\*Response (\d):\*\*\s*\"(.*?)\"\s*\* Accuracy: (\d+)\s*\* Relevance: (\d+)\s*\* Clarity: (\d+)\s*\* Depth: (\d+)\s*\*\*Score: ([\d\.]+)/10\*\*",
        value,
        re.DOTALL
    )

    # Start building HTML
    html = f'<div class="block" style="background:#fff8dc; border-left:5px solid orange; padding:1rem;">'
    html += f"<h3>🏆 Final Evaluation:</h3>"
    html += f"<p><strong>Best Model:</strong> <span style='color:#2563eb;'>{best_label}</span></p><br>"
    html += "<div style='display:grid; grid-template-columns: repeat(2, 1fr); gap: 1rem;'>"

    # Render each response card
    for response in response_blocks:
        resp_num, text, accuracy, relevance, clarity, depth, score = response
        model_name = response_map.get(f"Response {resp_num}", f"Response {resp_num}")

        html += "<div class='block' style='border:1px solid #ddd; padding:1rem; background:#fff;'>"
        html += f"<h4>{model_name}</h4>"
        html += f"<p>{text}</p>"
        html += "<ul style='margin-top: 10px;'>"
        html += f"<li><strong>Accuracy:</strong> {accuracy}</li>"
        html += f"<li><strong>Relevance:</strong> {relevance}</li>"
        html += f"<li><strong>Clarity:</strong> {clarity}</li>"
        html += f"<li><strong>Depth:</strong> {depth}</li>"
        html += "</ul>"
        html += f"<p><strong>Score:</strong> {score}/10</p>"
        html += "</div>"

    html += "</div></div>"
    return html
