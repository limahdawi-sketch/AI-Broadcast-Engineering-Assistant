from urllib.parse import quote

from fastapi import APIRouter
from schemas.assistant import DiagnoseRequest, DiagnoseResponse

router = APIRouter(prefix="/api/assistant", tags=["assistant"])


AR_INSTRUCTION = (
    "أنت مهندس خبير بمحطات الأرض الفضائية وأنظمة DSNG. "
    "حلّل الحالة كمهندس بث وأقمار اصطناعية متمرّس. "
    "حدّد الأسباب المحتملة بترتيب الأولوية، ثم خطوات الفحص والعلاج العملية "
    "بشكل مرقّم ومختصر. لا تفترض قيماً غير مذكورة. "
    "عند وجود خطر على الإرسال أو المعدات، اذكر التحذير بوضوح."
)

EN_INSTRUCTION = (
    "You are an expert Earth Station / DSNG broadcast engineer. "
    "Analyze the case like an experienced broadcast and satellite field engineer. "
    "Identify the most likely causes in priority order, then provide concise, "
    "numbered diagnostic and corrective steps. Do not invent missing measurements. "
    "Clearly flag any action that may risk the transmission or equipment."
)


@router.post("/diagnose", response_model=DiagnoseResponse)
def diagnose(payload: DiagnoseRequest):
    instruction = (
        AR_INSTRUCTION
        if payload.language == "ar"
        else EN_INSTRUCTION
    )

    prompt = f"""
{instruction}

Field case:

{payload.input}

Provide:
1. Most likely cause(s)
2. Recommended diagnostic checks
3. Corrective actions
4. Safety / operational caution where applicable

This is an engineering support response. Do not present assumptions as confirmed facts.
""".strip()

    encoded_prompt = quote(prompt, safe="")

    return DiagnoseResponse(
        prompt=prompt,
        chatgpt_url=f"https://chatgpt.com/?q={encoded_prompt}",
        claude_url=f"https://claude.ai/new?q={encoded_prompt}",
    )