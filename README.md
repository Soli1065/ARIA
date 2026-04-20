# ARIA

# ARIA v2 — Autonomous Reasoning and Intelligence Agent
> Living document. Update this as ARIA evolves. Last updated: 2026-04-19

---

## What Is ARIA?

ARIA is a modular autonomous AI agent with a physical body (SunFounder PiDog on Raspberry Pi).
It reasons, perceives, acts, remembers, and improves itself over time.
It is not a chatbot. It is not a remote-controlled robot. It is an agent — it decides what to do.

---

## Hardware

| Component | Status | Notes |
|---|---|---|
| Raspberry Pi 3B+ | ✅ On hand | Starting brain. 1GB RAM, limited local LLM |
| MicroSD card | ✅ On hand | Will be wiped and reflashed |
| Pi case + power adapter | ✅ On hand | Adapter replaced by PiDog battery later |
| SunFounder PiDog V2 | 🔜 Ordered | Body. Includes all sensors, servos, battery |
| Raspberry Pi 5 (8GB) | 📅 Future | Upgrade for full autonomy + local LLM |
| MacBook Air | ✅ On hand | Dev machine for Phase 1 |

---

## Architecture — 5 Layers

```
┌─────────────────────────────────┐
│     5. EXPRESSION LAYER         │  How ARIA communicates outward
├─────────────────────────────────┤
│     4. PERCEPTION LAYER         │  How ARIA senses the world
├─────────────────────────────────┤
│     3. MEMORY LAYER             │  What ARIA knows and remembers
├─────────────────────────────────┤
│     2. AGENT CORE               │  How ARIA thinks and decides
├─────────────────────────────────┤
│     1. FOUNDATION LAYER         │  What ARIA runs on
└─────────────────────────────────┘
```

### Layer 1 — Foundation
Runtime environment. Python, Ollama (local LLM), Claude API (cloud fallback), config, logging system.
Hardware-agnostic. Runs identically on Mac and Pi.

### Layer 2 — Agent Core
ARIA's brain.
- **ReAct Loop**: Perceive → Reason → Plan → Act → Observe → Reflect → repeat
- **Tool Dispatcher**: routes decisions to actions (move, speak, remember, search)
- **LLM Router**: decides local (Ollama) vs cloud (Claude API) per task
- **Self-Improvement Engine**: reflects on past cycles, updates behavioral patterns

### Layer 3 — Memory (3 tiers)
- **Working Memory**: current context window, active session state
- **Episodic Memory**: log of past interactions and outcomes (what happened, what worked)
- **Semantic Memory**: long-term learned knowledge, environment map, preferences

### Layer 4 — Perception
Inputs from the world. Mocked on Mac → real on PiDog.
- Camera → vision pipeline (OpenCV, MediaPipe)
- Microphone → speech-to-text (STT)
- Ultrasonic → obstacle distance
- IMU (6-DOF) → orientation and movement
- Touch sensor → physical contact detection
- Sound direction → locate audio source

### Layer 5 — Expression
Outputs to the world. Mocked on Mac → real on PiDog.
- Speaker → text-to-speech (TTS)
- 12 servos → movement, posture, gestures (32 actions)
- RGB LED → emotional state display
- FPV stream → real-time camera feed

---

## LLM Routing Strategy

```
Simple / fast / private tasks  →  Ollama local (free, instant, offline)
Complex reasoning               →  Claude API (powerful, costs tokens)
Unknown / sensitive             →  Claude API with local fallback
```

ARIA scores task complexity dynamically — routing is not hardcoded.

---

## Hardware ↔ ARIA Layer Mapping

| ARIA Layer | PiDog Hardware |
|---|---|
| Perception | Camera, mic, ultrasonic, IMU, touch, sound direction |
| Expression | Speaker, 12 servos, RGB LED |
| Foundation | Pi 3B+ (now) → Pi 5 8GB (later) |
| Memory | SD card file-based (now) → structured DB (later) |

---

## Pi 3B+ vs Pi 5 — Capability Comparison

| Capability | Pi 3B+ | Pi 5 (8GB) |
|---|---|---|
| Local LLM | ~1B model barely | 7B–13B comfortably |
| Vision pipeline | Basic OpenCV | Full MediaPipe + YOLO |
| Parallel tasks | 2–3 max | 6–8 simultaneously |
| Response speed | 3–8s per cycle | Sub-second locally |
| Full offline autonomy | ❌ Cloud-dependent | ✅ Yes |
| Self-improvement engine | Slow/limited | Full capability |
| Hailo AI HAT support | ❌ | ✅ 13 TOPS NPU |

On Pi 3B+: ARIA is a cloud-assisted smart companion.
On Pi 5: ARIA is a fully autonomous on-device agent.

---

## What ARIA Can Do (Final Vision on PiDog + Pi 5)

1. **Conversational intelligence** — hears, understands context, remembers history, responds with personality
2. **Environmental awareness** — builds spatial map, recognizes faces, tracks objects and sounds
3. **Embodied emotion** — expresses internal state through body language, LED, posture — driven by reasoning not scripts
4. **Autonomous patrol & exploration** — navigates, avoids obstacles, investigates, logs findings
5. **Self-improvement** — reflects after each session, updates behavior patterns, gets better over time
6. **Private by default** — sensitive reasoning stays on-device, cloud used by choice
7. **Expandable tool system** — new sensors, APIs, behaviors plug in cleanly without breaking existing layers

---

## Development Roadmap

```
Phase 1 — ARIA Core on MacBook        ← YOU ARE HERE
Phase 2 — Migrate to Raspberry Pi
Phase 3 — PiDog Integration
Phase 4 — Pi 5 Upgrade + Full Autonomy
Phase 5 — Expansion (sensors, skills, integrations)
```

---

## Phase 1 — ARIA Core on MacBook

**Goal**: ARIA's brain works completely before touching any hardware.
All hardware replaced by mocks. Logs visible at every step.

### Steps

#### Step 1.1 — Project Structure
Set up the ARIA Python project with clean folder layout.
Define all modules as empty stubs so the shape of the system is clear from day one.

#### Step 1.2 — Foundation Layer
- Python environment (venv)
- Config system (API keys, model selection, environment flags)
- **Logging system** — structured, timestamped, visible at every layer
- Ollama install + first local model running
- Claude API connection verified

#### Step 1.3 — Mock Perception & Expression
Replace all hardware sensors/actuators with mock functions.
Mocks return realistic fake data (random distance readings, fake speech input, logged fake movements).
This lets the full loop run on Mac without any Pi or PiDog.

#### Step 1.4 — Memory Layer
- Working memory (in-memory dict/context)
- Episodic memory (append-only log file)
- Semantic memory (simple JSON store to start)
Read/write tested independently before connecting to agent.

#### Step 1.5 — Tool Dispatcher
Define ARIA's tool registry — every action ARIA can take is a named tool.
Tools at this stage: speak, move, remember, recall, observe, reflect.
Dispatcher routes LLM decisions to the right tool function.

#### Step 1.6 — LLM Router
Logic that scores a task and routes to Ollama or Claude API.
Tested with sample prompts to verify routing decisions make sense.

#### Step 1.7 — ReAct Loop
Wire everything together into the full Perceive → Reason → Plan → Act → Observe → Reflect cycle.
Run end-to-end on Mac with mocks. ARIA should complete full reasoning cycles visibly in logs.

#### Step 1.8 — Self-Improvement Engine (stub)
Basic reflection module: after N cycles, ARIA reviews episodic memory and writes a reflection.
Full implementation comes later — stub ensures the hook is in place.

#### Step 1.9 — Validation
Run ARIA through a set of test scenarios on Mac.
Verify logs show every step clearly.
Confirm the system is stable and ready for Pi migration.

### Phase 1 Success Criteria
- [ ] ARIA completes full ReAct cycles autonomously on Mac
- [ ] Every layer logs its activity with timestamps
- [ ] LLM routing works (local + cloud)
- [ ] Memory reads and writes correctly across cycles
- [ ] All hardware calls go through mocks (zero real hardware dependency)
- [ ] Codebase is clean, modular, ready to migrate

---

## Logging Philosophy

ARIA logs everything. Every cycle, every decision, every tool call, every memory read/write.
Log format: `[TIMESTAMP] [LAYER] [LEVEL] message`

Example:
```
[2026-04-19 14:32:01] [PERCEPTION] [INFO]  Sound detected at 45° — intensity: 72dB
[2026-04-19 14:32:01] [AGENT_CORE] [INFO]  Cycle 42 started
[2026-04-19 14:32:02] [LLM_ROUTER] [INFO]  Task complexity: 0.3 → routing to Ollama
[2026-04-19 14:32:03] [AGENT_CORE] [INFO]  Reasoning complete → tool selected: move_toward_sound
[2026-04-19 14:32:03] [EXPRESSION] [INFO]  Action: move_toward_sound(angle=45)
[2026-04-19 14:32:03] [MEMORY]     [INFO]  Episodic write: cycle_42 → moved_toward_sound
[2026-04-19 14:32:04] [AGENT_CORE] [INFO]  Observation: obstacle at 18cm
[2026-04-19 14:32:04] [AGENT_CORE] [INFO]  Cycle 42 complete
```

Logs visible in terminal during dev. Written to file always. Later: optional web dashboard.

---

## Project Folder Structure (Target)

```
aria/
├── README.md                  ← this file (living doc)
├── config/
│   └── settings.py            ← API keys, model config, env flags
├── foundation/
│   └── logger.py              ← ARIA logging system
├── agent_core/
│   ├── react_loop.py          ← main reasoning cycle
│   ├── llm_router.py          ← local vs cloud routing
│   ├── tool_dispatcher.py     ← tool registry and execution
│   └── self_improvement.py   ← reflection engine
├── memory/
│   ├── working.py             ← current context
│   ├── episodic.py            ← interaction log
│   └── semantic.py            ← long-term knowledge store
├── perception/
│   ├── mock.py                ← Mac dev mocks
│   ├── camera.py              ← vision pipeline
│   ├── microphone.py          ← STT
│   ├── ultrasonic.py          ← distance
│   ├── imu.py                 ← orientation
│   ├── touch.py               ← contact
│   └── sound_direction.py    ← audio localization
├── expression/
│   ├── mock.py                ← Mac dev mocks
│   ├── speaker.py             ← TTS
│   ├── movement.py            ← servo actions
│   └── led.py                 ← emotion display
├── tools/
│   └── registry.py            ← all ARIA tools defined here
├── tests/
│   └── test_react_loop.py     ← Phase 1 validation scenarios
└── logs/
    └── aria.log               ← persistent log output
```

---

## Decision Log

Track key decisions made during development so we never lose context.

| Date | Decision | Reason |
|---|---|---|
| 2026-04-19 | PiDog V2 chosen as body | Most complete sensor suite, Ollama native, open source |
| 2026-04-19 | Pi 3B+ for Phase 1–3 | Already owned, sufficient for cloud-assisted ARIA |
| 2026-04-19 | Pi 5 8GB planned for Phase 4 | Full autonomy, local 7B+ LLM, Hailo HAT support |
| 2026-04-19 | Claude API as primary cloud LLM | Best reasoning quality, already integrated |
| 2026-04-19 | Ollama for local LLM | Free, private, runs on Pi |
| 2026-04-19 | Mac-first development | Build brain before body, mocks replace hardware |
| 2026-04-19 | File-based memory to start | Simple, portable, easy to inspect and debug |

---

## Open Questions / Future Decisions

- [ ] Which Ollama model to start with on Pi 3B+? (1B candidates: qwen2.5:1.5b, tinyllama)
- [ ] Web dashboard for logs — when to add?
- [ ] Voice wake word for ARIA ("Hey ARIA") — Phase 3 or later?
- [ ] Smart home integrations — which Phase?
- [ ] PiDog V2 order — confirm shipped with Robot HAT 5 for future Pi 5 compatibility

---

*ARIA is a living system. This document grows with it.*
