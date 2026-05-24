# Code Generation Plan — Unit 4: Reminder Form Integration

## Unit Context

**Unit**: Unit 4 — Reminder Form Integration
**Responsibility**: Add reminder time input to the todo form. Display reminder time on todo cards. Visual indicator when a todo has an upcoming or overdue reminder.

**Stories Implemented**:
- US-1 (frontend): Datetime-local input in TodoForm for reminder_at
- US-2: Display reminder time on TodoItem + ReminderBadge

**Dependencies**:
- Unit 2's API contracts (Todo model includes `reminder_at` in responses)

**Files to Modify/Create**:
| File | Action |
|---|---|
| `frontend/types/index.ts` | Modify — add `reminder_at` to Todo interface |
| `frontend/components/TodoForm.vue` | Modify — add datetime-local input for reminder_at |
| `frontend/components/ReminderBadge.vue` | Create — visual badge (upcoming/due) |
| `frontend/components/TodoItem.vue` | Modify — display reminder time + ReminderBadge |
| `frontend/pages/dashboard.vue` | Modify — pass reminder_at in create form |

---

## Execution Steps

### Step 1: Modify frontend/types/index.ts — Add reminder_at to Todo interface
- [x] Add `reminder_at: string | null` to Todo interface
- [x] Add `reminder_at?: string` to TodoCreate type
- [x] Add `reminder_at?: string | null` to TodoUpdate type

### Step 2: Create frontend/components/ReminderBadge.vue — Visual badge component
- [ ] Create component accepting `reminder_at` and `status` props
- [ ] Show "upcoming" badge when reminder_at is in the future and status != done
- [ ] Show "due" badge when reminder_at is in the past and status != done
- [ ] Show nothing when reminder_at is null or status is done
- [ ] Add data-testid attributes for automation

### Step 3: Modify frontend/components/TodoForm.vue — Add reminder datetime input
- [ ] Add `reminder_at` field to form reactive state
- [ ] Add datetime-local input in the form template
- [ ] Populate reminder_at when editing existing todo
- [ ] Include reminder_at in submit data for both create and edit
- [ ] Support clearing reminder_at (set to null/undefined)

### Step 4: Modify frontend/components/TodoItem.vue — Display reminder + badge
- [ ] Import and use ReminderBadge component
- [ ] Display formatted reminder_at time in meta info row
- [ ] Show ReminderBadge next to reminder time

### Step 5: Modify frontend/pages/dashboard.vue — Pass reminder_at in create form
- [ ] Add `reminder_at` to createForm reactive
- [ ] Add datetime-local input in the inline create form
- [ ] Include reminder_at in handleCreateTodo data
- [ ] Reset reminder_at in resetCreateForm
- [x] Display ReminderBadge in todo list items

### Step 6: Generate code summary documentation
- [ ] Create `aidlc-docs/construction/unit-4/code/code-summary.md`

---

## Acceptance Criteria Verification
- [x] TodoForm has optional datetime-local input for reminder
- [x] Reminder can be set during create and edit
- [x] Reminder can be cleared (set to null)
- [x] TodoItem shows formatted reminder_at when set
- [x] ReminderBadge shows "upcoming" (future) or "due" (past, not done)
- [x] No badge when reminder_at is null
- [x] Form submits reminder_at in correct ISO 8601 format
- [x] Todo TypeScript interface includes `reminder_at: string | null`
