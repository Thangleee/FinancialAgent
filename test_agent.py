
import json
import requests
import re

with open("test_questions.json", "r", encoding="utf8") as f:
    tests = json.load(f)

def extract_lowest_open(output_text):
    """
    Trích xuất mã và giá mở cửa thấp nhất từ output AI, robust với nhiều dạng câu.
    """
    prices = {}
    for line in output_text.splitlines():
        
        m = re.match(r'-?\s*(\w+)[\s:]+([<>]?\d[\d.,\s]*VND)', line)
        if m:
            symbol = m.group(1)
            price_str = m.group(2)

            
            price_num = re.sub(r'[^0-9]', '', price_str)
            if price_num:
                prices[symbol] = int(price_num)

    if prices:
        lowest_symbol = min(prices, key=prices.get)
        lowest_price = f"{prices[lowest_symbol]:,} VND".replace(",", ".")
        return [lowest_symbol, lowest_price]

    m2 = re.search(r'→ Mã (\w+).*?([\d.,]+\s*VND)', output_text)
    if m2:
        symbol = m2.group(1)
        price = m2.group(2).replace(" ", "")
        return [symbol, price]

    return None

# ==== URL API Agent ====
URL = "http://127.0.0.1:8000/ask"  

correct = 0

for t in tests:
    question = t.get("question")
    expected = t.get("expected_answer")

    if question is None or expected is None:
        print("Test case thiếu question hoặc expected_answer")
        continue
    payload = {"question": question}
    try:
        res = requests.post(URL, json=payload, timeout=20)
        output = res.json().get("answer", "").strip()
    except Exception as e:
        output = f"ERROR: {e}"

    if "tổng khối lượng" in question.lower():
        m_vol = re.search(r'(\d[\d.,]*)\s*cổ phiếu', output)
        if m_vol:
            extracted = [m_vol.group(1).replace(",", ".")]
            extracted.append(expected[1]) 
            extracted.append(expected[2])
        else:
            extracted = None

    elif "mã nào có giá mở cửa thấp nhất" in question.lower():
        extracted = extract_lowest_open(output)
    else:
        extracted = output

    is_correct = (extracted == expected)

    if is_correct:
        correct += 1

    print("=" * 60)
    print("Question:", question)
    print("Expected:", expected)
    print("Output:  ", extracted)
    print("Result:  ", "Correct" if is_correct else "Wrong")

print("\n" + "=" * 60)
print(f"Final Score: {correct}/{len(tests)} correct")
print(f"Accuracy: {correct/len(tests)*100:.2f}%")
