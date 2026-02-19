"""
Lab 05: AI Travel Planner Bot - 10 Auto-grading Tests
ตรวจสอบโครงสร้างไฟล์ workflow.json โดยไม่ต้องรัน n8n
"""

import pytest
import json
import os

WORKFLOW_FILE = 'workflow.json'


class TestWorkflowFile:
    """ตรวจสอบไฟล์ workflow.json (16 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
        else:
            self.workflow = None
            self.nodes = []

    def test_01_workflow_file_exists(self):
        """Test 1: มีไฟล์ workflow.json (8 คะแนน)"""
        assert os.path.exists(WORKFLOW_FILE), \
            "workflow.json not found - กรุณา export workflow จาก n8n"

    def test_02_workflow_valid_json(self):
        """Test 2: เป็น valid JSON (8 คะแนน)"""
        assert self.workflow is not None, "workflow.json is not valid JSON"
        assert 'nodes' in self.workflow, "workflow.json missing 'nodes' key"
        assert 'connections' in self.workflow, "workflow.json missing 'connections' key"


class TestWebhookNode:
    """ตรวจสอบ Webhook Node (18 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
        else:
            self.workflow = None
            self.nodes = []

    def test_03_has_webhook_node(self):
        """Test 3: มี Webhook Node (10 คะแนน)"""
        webhook_nodes = [n for n in self.nodes
                         if n.get('type', '').lower().replace('.', '').find('webhook') != -1]
        assert len(webhook_nodes) > 0, \
            "ไม่พบ Webhook Node - ต้องมี Webhook เพื่อรับข้อความจาก bot.py"

    def test_04_webhook_post_method(self):
        """Test 4: Webhook ใช้ POST method (8 คะแนน)"""
        webhook_nodes = [n for n in self.nodes
                         if n.get('type', '').lower().replace('.', '').find('webhook') != -1]
        assert len(webhook_nodes) > 0, "ไม่พบ Webhook Node"
        webhook = webhook_nodes[0]
        params = webhook.get('parameters', {})
        method = params.get('httpMethod', '').upper()
        assert method == 'POST', \
            f"Webhook ต้องใช้ POST method (พบ: {method})"


class TestAPINodes:
    """ตรวจสอบ API Nodes (34 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
        else:
            self.workflow = None
            self.nodes = []

    def _get_all_node_text(self):
        """รวมข้อมูลทุก node เป็น text เพื่อค้นหา"""
        texts = []
        for node in self.nodes:
            texts.append(json.dumps(node, ensure_ascii=False).lower())
        return texts

    def test_05_has_weather_api(self):
        """Test 5: มี HTTP Node สำหรับ OpenWeatherMap (10 คะแนน)"""
        node_texts = self._get_all_node_text()
        has_weather = any('openweathermap' in t or 'weather' in t
                          for t in node_texts)
        assert has_weather, \
            "ไม่พบ HTTP Node ที่เรียก OpenWeatherMap API"

    def test_06_has_ai_node(self):
        """Test 6: มี AI Node - Basic LLM Chain หรือ OpenRouter (14 คะแนน)"""
        node_texts = self._get_all_node_text()
        # Check for Basic LLM Chain node
        has_llm_chain = any('chainllm' in t or 'chain_llm' in t or 'lmchatopenrouter' in t
                            for t in node_texts)
        # Check for HTTP Request to OpenRouter (backward compatible)
        has_openrouter_http = any('openrouter' in t for t in node_texts)
        assert has_llm_chain or has_openrouter_http, \
            "ไม่พบ AI Node (Basic LLM Chain + OpenRouter Chat Model หรือ HTTP Request ไป openrouter.ai)"

    def test_07_has_places_api(self):
        """Test 7: มี HTTP Node สำหรับ Geoapify Places (10 คะแนน)"""
        node_texts = self._get_all_node_text()
        has_places = any('geoapify' in t or 'places' in t
                         for t in node_texts)
        assert has_places, \
            "ไม่พบ HTTP Node ที่เรียก Geoapify Places API"


class TestCodeAndDiscord:
    """ตรวจสอบ Code Node และ Discord (32 คะแนน)"""

    @pytest.fixture(autouse=True)
    def load_workflow(self):
        if os.path.exists(WORKFLOW_FILE):
            with open(WORKFLOW_FILE, 'r', encoding='utf-8') as f:
                self.workflow = json.load(f)
                self.nodes = self.workflow.get('nodes', [])
        else:
            self.workflow = None
            self.nodes = []

    def test_08_has_code_node(self):
        """Test 8: มี Code Node (10 คะแนน)"""
        code_nodes = [n for n in self.nodes
                      if 'code' in n.get('type', '').lower()]
        assert len(code_nodes) > 0, \
            "ไม่พบ Code Node - ต้องมีสำหรับ Format Embed หรือ Parse Extract"

    def test_09_has_discord_webhook(self):
        """Test 9: มี HTTP Node สำหรับ Discord (10 คะแนน)"""
        node_texts = [json.dumps(n, ensure_ascii=False).lower() for n in self.nodes]
        has_discord = any('discord' in t for t in node_texts)
        assert has_discord, \
            "ไม่พบ HTTP Node ที่ส่งข้อมูลไป Discord Webhook"

    def test_10_code_has_embed(self):
        """Test 10: Code Node มีการสร้าง Discord Embed (12 คะแนน)"""
        code_nodes = [n for n in self.nodes
                      if 'code' in n.get('type', '').lower()]
        assert len(code_nodes) > 0, "ไม่พบ Code Node"

        # Check if any code node contains embed-related keywords
        has_embed = False
        for node in code_nodes:
            js_code = node.get('parameters', {}).get('jsCode', '')
            if any(keyword in js_code.lower()
                   for keyword in ['embed', 'fields', 'color', 'title', 'description']):
                has_embed = True
                break
        assert has_embed, \
            "Code Node ไม่มีการสร้าง Discord Embed (ต้องมี embeds, fields, color)"
