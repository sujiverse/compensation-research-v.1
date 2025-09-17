---
layout: default
title: 보상작용 연구 허브 - 자동화 시스템
description: 10분마다 자동 업데이트되는 보상작용 연구 데이터베이스
---

# 🧠 보상작용 연구 자동화 시스템

<div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; border-radius: 10px; margin: 20px 0;">
  <h2 style="margin: 0; color: white;">🤖 실시간 자동 연구 시스템</h2>
  <p style="margin: 10px 0 0 0;">OpenAlex API 기반 • 10분마다 자동 업데이트 • 5WHY 분석 • 크로스체크 가이드</p>
</div>

## 📊 현재 현황

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0;">
  <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #28a745;">
    <h3 style="margin: 0; color: #28a745;">📄 수집된 논문</h3>
    <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">{{ site.pages | where: "dir", "/papers/" | size }}</p>
  </div>
  <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #007bff;">
    <h3 style="margin: 0; color: #007bff;">🧠 학습된 규칙</h3>
    <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">자동 추출</p>
  </div>
  <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #ffc107;">
    <h3 style="margin: 0; color: #ffc107;">🔄 업데이트 주기</h3>
    <p style="font-size: 24px; font-weight: bold; margin: 5px 0;">10분마다</p>
  </div>
  <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #dc3545;">
    <h3 style="margin: 0; color: #dc3545;">⏰ 마지막 업데이트</h3>
    <p style="font-size: 14px; font-weight: bold; margin: 5px 0;">{{ "now" | date: "%Y-%m-%d %H:%M" }}</p>
  </div>
</div>

## 🔗 주요 링크

<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 15px; margin: 20px 0;">
  <a href="./보상작용.html" style="text-decoration: none;">
    <div style="background: #e3f2fd; padding: 20px; border-radius: 8px; border: 1px solid #2196f3;">
      <h3 style="margin: 0; color: #1976d2;">📋 보상작용 허브</h3>
      <p style="color: #666; margin: 5px 0 0 0;">모든 논문과 템플릿의 중심 허브</p>
    </div>
  </a>
  <a href="./papers/" style="text-decoration: none;">
    <div style="background: #f3e5f5; padding: 20px; border-radius: 8px; border: 1px solid #9c27b0;">
      <h3 style="margin: 0; color: #7b1fa2;">📄 논문 컬렉션</h3>
      <p style="color: #666; margin: 5px 0 0 0;">자동 수집된 연구 논문들</p>
    </div>
  </a>
  <a href="./보상작용-규칙(자동).html" style="text-decoration: none;">
    <div style="background: #fff3e0; padding: 20px; border-radius: 8px; border: 1px solid #ff9800;">
      <h3 style="margin: 0; color: #f57c00;">🧠 자동 학습 규칙</h3>
      <p style="color: #666; margin: 5px 0 0 0;">AI가 추출한 보상 패턴들</p>
    </div>
  </a>
  <a href="./5WHY-보상작용-템플릿.html" style="text-decoration: none;">
    <div style="background: #e8f5e8; padding: 20px; border-radius: 8px; border: 1px solid #4caf50;">
      <h3 style="margin: 0; color: #388e3c;">📝 5WHY 템플릿</h3>
      <p style="color: #666; margin: 5px 0 0 0;">체계적 원인 분석 가이드</p>
    </div>
  </a>
</div>

## 🚀 **자동화 기능**

### 🔄 **10분마다 자동 실행**
- OpenAlex API에서 최신 논문 수집
- 신뢰도 점수 자동 계산
- 근육간 보상 패턴 학습
- Obsidian 노드 자동 생성
- GitHub Pages 자동 배포

### 🧠 **5WHY 분석 시스템**
각 논문마다 체계적인 5단계 원인 분석:
1. **1차**: 통증/제한 발생 원인
2. **2차**: 특정 근육 약화 원인
3. **3차**: 근육 불균형 원인
4. **4차**: 보상작용 발생 원인
5. **5차**: 패턴 고착화 원인

### 🎯 **크로스체크 가이드**
- **MMT**: Manual Muscle Testing
- **Movement**: 기능적 움직임 스크린
- **ROM**: 관절가동범위 검사
- **Special Tests**: 특수 진단 검사

## 📈 **실시간 모니터링**

<div style="background: #f8f9fa; padding: 20px; border-radius: 8px; margin: 20px 0;">
  <h3>🔍 시스템 상태</h3>
  <ul>
    <li><strong>API 상태</strong>: OpenAlex 연결 활성</li>
    <li><strong>자동화</strong>: GitHub Actions 실행 중</li>
    <li><strong>웹사이트</strong>: GitHub Pages 활성</li>
    <li><strong>데이터</strong>: 실시간 동기화</li>
  </ul>
</div>

## 🛠️ **기술 스택**

- **Backend**: Python 3.11 + OpenAlex API
- **자동화**: GitHub Actions (10분 주기)
- **웹사이트**: GitHub Pages + Jekyll
- **문서**: Obsidian Markdown + 5WHY 분석
- **AI**: 자동 규칙 학습 + 패턴 추출

---

<div style="text-align: center; margin: 40px 0; padding: 20px; background: #f1f3f4; border-radius: 8px;">
  <p style="color: #666; margin: 0;"><strong>🤖 이 사이트는 GitHub Actions로 10분마다 자동 업데이트됩니다.</strong></p>
  <p style="color: #888; margin: 5px 0 0 0; font-size: 14px;">마지막 업데이트: {{ "now" | date: "%Y-%m-%d %H:%M UTC" }}</p>
</div>