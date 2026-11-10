# Code review: 3D Cannonball Flight Simulator

This file holds the reviews newest first: the second recheck, the recheck, the follow-up review, then the original review.

# Second recheck

## Grade: B+ (up from B)

**The landing check is now reliable, and the small fixes listed in the recheck are almost all in.** `C++ Sim/src/Simulation.cpp` and `Python Code/run_simulation.py` changed, and the C++ builds with zero warnings. The binary in `cmake-build-debug/` was up to date at the time of review. What's holding this at B+ is the lack of tests and the unvalidated config read in `main.cpp`.

## What's verified

| Item | Status | Evidence |
|---|---|---|
| Landing detection | **Fixed** | Wrong in 0 of 631 cases, using the real engine and script logic |
| `v0=100, dt=0.1, T=20` | **Fixed** | Now shows "Target hit!" instead of a false "mid-air" |
| Box proportions | **Fixed** | All three axes are equal, and the limits are shared |
| Deprecation warning | **Fixed** | 0 warnings across the whole test run |
| Misleading error message | **Fixed** | The message now includes the actual system error |
| Read-only folder traceback | **Fixed** | Shows a clean error |
| Empty CSV traceback | **Fixed** | Shows a clean error |
| Error above green banner | **Fixed, with a side effect** | See issue 2 |
| Session isolation | **Still holding** | Session A kept its own shot |

The race test had no tracebacks this time, though the race itself remains (see "Still open").

## Remaining issues

1. **One-row shots still show "Target hit!" over a blank plot.** This is the only false success still reachable from the UI. θ=0 and `dt=100` both do it, because the `len(df) < 2` guard wasn't added. Put this before the plotting code:

   ```python
   if len(df) < 2:
       st.warning("No flight: fewer than two data points. Check the launch angle and time step.")
   ```

   The rest of the plotting block then goes under an `else`. The guard also fixes the header-only CSV crash below, and it makes the `if not df.empty else 0` on line 94 removable. That check can't help, because an empty `df` crashes at line 78 first.

2. **A failed shot loses the last good plot again.** The recheck marked this fixed, but Fire now clears `df` up front (line 28) and the `elif` on line 68 hides the plot.
   - This is a reasonable choice, since it also removed the contradictory banner, so it can stay.
   - To keep the old plot instead, stop clearing **both** `df` and `landed`. Clearing only `df` would make a good old shot show a false "mid-air" warning.

3. **Two malformed-CSV cases still give tracebacks.** Both were forced with a stub engine, and neither appeared in the race test.
   - A header-only CSV raises `ValueError`, which the guard above fixes.
   - A ragged row raises `ParserError`. Add `pd.errors.ParserError` to the `EmptyDataError` handler on line 57.

4. **A missing status line reads as "mid-air".** A binary built before this change prints neither `landed` nor `max_time`, so the app shows a false warning. The current binary is fine, but this could catch someone after an old checkout. Treating a missing status as an error would make that obvious.

## Still open

- **Config validation:** a config of `abc` still exits 0 and now reports `landed`. Nothing validates anything except `dt`, so use the checked read from the follow-up review.
- **Shared-file race:** in 300 fires from two sessions, 201 were correct, 66 showed the wrong data as a success and 33 showed an error. Only CLI args and stdout fix this.
- **Engine output:**
  - Failed writes still print "Success".
  - Time still drifts.
  - The landing point isn't interpolated.
  - Timed-out runs leave a large CSV (226 MB here).
- **Project:**
  - The README run path and "Euler" wording are out of date.
  - There's no `requirements.txt`.
  - Generated files and `.idea/` are still tracked.
- **Comments:** several still narrate history ("Moved…", "Restored…", "Updated to…"). Those belong in commit messages.

## Next steps

1. **Commit now.** Three rounds of fixes existed only as uncommitted changes on a USB drive at the time of review, and that's the biggest risk to this project. Add the `len(df) < 2` guard first if wanted, but don't wait on anything else.
2. **Fix `main.cpp`'s read validation.** It's about 3 lines.
3. **Start the unit tests.** The UI is now in good shape, so more polish there has little value. The 631-case sweep is a ready-made first test: compare the engine's landed status with the analytic flight time.

**Limits of this recheck:** the code was built with `clang++` instead of `cmake`, and the UI was driven through `AppTest`, not a real browser.

---

# Recheck

## Grade: B (up from B−)

**Five of the six bugs from the follow-up review are fixed, and the sixth is mostly there.** Only `Python Code/run_simulation.py` changed since the follow-up. The C++, README and `CMakeLists.txt` are the same, and all of it was uncommitted at the time of review.

To reach a B+, the app needs a reliable landing check and the few small fixes below. After that, the missing tests are what's holding it back.

## Status of the six bugs

| # | Bug | Status | Evidence |
|---|---|---|---|
| 1 | Sessions showing each other's data | **Fixed** | After B fired at 200 m/s, A stayed on its 50 m/s shot |
| 2 | Missing binary traceback | **Fixed** | Missing and non-executable binaries both show a clean error |
| 3 | Failed shot wipes the plot | **Fixed** | The plot and error both survive the next interaction |
| 4 | False "Target hit!" | **Partly fixed** | `v0=100` now warns correctly, but see issue 1 below |
| 5 | Negative flight time crash | **Fixed** | A forced `T=-1` was rejected and the shot ran at the default |
| 6 | Graph scale | **Mostly fixed** | The 1e-14 axis is gone, but see issue 2 below |

## New or remaining issues

1. **`last_y <= 0.5` misjudges landings (`Python Code/run_simulation.py:85`).** The last row's height depends on speed and `dt`, so no fixed threshold works.
   - Across 631 parameter combinations, it gave 70 false "mid-air" warnings and 2 false "Target hit!" results. The grid was deliberately wide, so normal use will be better than that.
   - For example, `v0=100, dt=0.1, T=20` lands but reports "mid-air".
   - θ=0 and `dt=100` still show "Target hit!" over a blank plot.

2. **`set_box_aspect` was removed, so height is drawn too short.** Matplotlib's default box is 4:4:3, so the vertical axis is squashed by 25%. The snippet in the follow-up review showed only the limits and didn't say to keep this line. Put `ax.set_box_aspect([1, 1, 1])` back.

3. **The deprecation warning is still there (`Python Code/run_simulation.py:92`).** Passing `use_container_width` at all triggers it, even as `False`, and the comment above says `width="stretch"` while the code uses 1500. Use `st.dataframe(df, width="stretch")`.

4. **The `OSError` message can blame the wrong thing (`Python Code/run_simulation.py:52-54`).** `read_csv` is inside that `try`, so a file-read failure reports "Could not find or execute C++ binary". Include `{e}` and word it more generally.

5. **Some failures still give a raw traceback.** The UI inputs can't produce these directly, but the first and third can occur with a race or a read-only folder:
   - An empty CSV raises `EmptyDataError`.
   - A header-only CSV raises `ValueError`.
   - `os.remove` and `open` at lines 30-34 sit outside the `try`, so a read-only folder crashes the app.

6. **An error can sit above a green success banner.** After a failed shot, the old plot still shows "Target hit!" under the error, which reads as a contradiction.

**Still open from before:**

- **Concurrent fires:** in 300 fires from two sessions, 50 showed the wrong data as a success, and 15 gave an error or traceback caused by the race. Only moving off shared files fixes this.
- **Engine and output:**
  - `main.cpp` still doesn't validate the read.
  - Failed writes still print "Success".
  - Time still drifts.
  - The landing point still isn't interpolated.
  - A timed-out run still leaves a large partial CSV (220 MB here).
- **Project:**
  - The README's run path and "Euler" wording are out of date.
  - There's no `requirements.txt`.
  - Generated files are still tracked.
  - The "Fix:" and "Claude's math" comments belong in commit messages, not the code.

## Correction: the earlier landing check was worse

The scratch fix from the follow-up review used `t + dt > T`, and it was reported as behaving correctly after only a few shots. In this sweep it was wrong in **124 of 631** cases, against 72 for the `last_y` rule, so it should not be used.

## The fix for landing detection

Only the engine knows why its loop stopped, so it should say so. Add this after the loop in `C++ Sim/src/Simulation.cpp`, then rebuild:

```cpp
std::cout << (ball.y < 0 ? "landed\n" : "max_time\n");
```

Then read it in Python and store it next to the DataFrame:

```python
result = subprocess.run(...)
st.session_state.landed = "landed" in result.stdout.splitlines()
```

This was **wrong in 0 of the same 631 cases**. That sweep skips shots landing within two time steps of the limit, where the correct answer is ambiguous.

This was tested together with fixes for issues 2–6 on a scratch copy, and these then behaved correctly:

- θ=0, `dt=100` and a header-only CSV show a "No flight" warning.
- An empty CSV and a read-only folder show clean errors.
- A failed shot shows "Showing the last successful shot" instead of the green banner.
- There are no deprecation warnings.

## Next steps

1. Apply the landing fix and issues 2–6, about 20 lines in total.
2. Add unit tests, as planned in the follow-up review. This sweep is a good model: the earlier landing check looked fine until it was run across many cases. A test comparing landed status with the analytic flight time would have caught both rules.
3. Move to CLI args and stdout, which removes the remaining race.

**Limits of this recheck:** the code was built with `clang++` instead of `cmake`, and the UI was driven through `AppTest`, not a real browser.

---

# Follow-up review

## Updated grade: B−

This is up from a C. **The physics is now correct**, and the hang is gone from the UI. It stops short of a solid B for three reasons:

- The new session state introduced a bug where one session can show another session's data.
- The missing-binary error handling was lost.
- The app still says "Target hit!" for shots that never landed.

These take about 25 lines to fix, and the fixes were tested on a scratch copy of the script. They have not been applied to the repo.

## Fix verification

| Fix | Verdict | Evidence |
|---|---|---|
| Physics and axes | **Fixed** | Apex and range are the same at every azimuth tested, and heights match the analytic value to within CSV rounding (5e-5 m) |
| Infinite loop | **Fixed in the UI** | `dt=0`, negative, `abc` and `nan` all exit 1 with a clear message, and a forced `dt=0` never reached the engine |
| Stale data | **Fixed** | If no CSV is produced, the app now reports it instead of showing old data |
| Timeout | **Works, with a leftover** | It fired at 5.0 s and showed an error, but left a **234 MB** partial CSV on disk |
| Vanishing UI | **Works, but caused a new bug** | The plot survives slider moves, but see bug 1 below |
| Graph scaling | **Not fixed** | The default shot's X axis still spans about 1e-14 |

### Bugs to fix now

1. **New: sessions can show each other's data (`Python Code/run_simulation.py:46-48`).** `session_state` stores only a flag, so every rerun re-reads the shared CSV.
   - Session A fired at 50 m/s and session B at 200 m/s. When A moved a slider, **A's plot switched to the 200 m/s shot**. This needs no timing luck, just a second tab.
   - If the file is gone, A shows "trajectory.csv was not found."
   - Fix: read the CSV once in the Fire block and keep the DataFrame in `st.session_state`.

2. **Regression: a missing binary now gives a raw traceback.** `except FileNotFoundError` was dropped, so anyone running the app before building hits this. A non-executable binary does the same. Catch `OSError`.

3. **A failed shot destroys the last good result.** The CSV is deleted before the run and `sim_run` is reset, so the old plot disappears. The error message also vanishes on the next interaction, leaving a blank page. Storing the DataFrame fixes this too.

4. **False success is still there.** At the default 10 s limit, any 45° shot above about 69 m/s stops in mid-air. At 100 m/s the last row is **216.6 m up**, and the app says "Target hit!". The same message appears over a blank plot for θ=0 and `dt=100`, which each give one row.

5. **Negative Max Flight Time crashes the app.** `T=-1` writes a header-only CSV, and Matplotlib raises a `TypeError`. From the code, this should repeat on every rerun until the next shot, because `sim_run` stays true. Add `min_value` to that input.

6. **`set_box_aspect` doesn't do what was intended.** It fixes the shape of the box, not the scale of the axes. X still spans 1e-14 and is drawn as long as the 273 m Z axis. Shared limits fix it:

   ```python
   span = max(df['x'].max() - df['x'].min(), df['z'].max() - df['z'].min(), df['y'].max(), 1.0)
   cx = (df['x'].max() + df['x'].min()) / 2
   cz = (df['z'].max() + df['z'].min()) / 2
   ax.set_xlim(cx - span/2, cx + span/2)
   ax.set_ylim(cz - span/2, cz + span/2)
   ax.set_zlim(0, span)
   ```

### Remaining edge cases

- **Concurrent fires still race.** Over 200 fires from two sessions, 99 returned the other session's data while showing success. Only removing the shared files fixes this.
- **Landing point:** the last row is still above ground, 0.28 m high and 0.28 m short at 45°. At θ=1° that's 8.50 m against 8.89 m, about 4% short.
- **`main.cpp` still accepts bad input.** `abc 45 90 0.01 10` sets `v0` to 0, exits 0 and gives one row. Empty and short files print "loaded params" and run on defaults. A tiny `dt` like `1e-300` still ran past the 2 s limit, though only by hand-editing the config, since the UI blocks it.
- **Failed writes:** the engine still prints "Success" and exits 0. The app now catches this only because the file is missing.
- **Time drift:** `dt=0.001, T=1` still gives 1000 rows, not 1001.

### Correction to the first review

The first review said plotting `(x, z, y)` would make azimuth look reversed. That was wrong. The axis labels match the data, and φ increases counter-clockwise from +X seen from above, which is the normal convention, so that line can stay. The claim is corrected in the original review below.

## Code quality

**`C++ Sim/src/CannonBall.cpp`: good.**

- The physics and update order are correct, and `toRadians` is now properly in an anonymous namespace.
- Strict warnings dropped to zero, and ASan/UBSan were clean on the two configs run.
- Make `pi` and `gravity` `constexpr`, and use a constructor initializer list.
- Rename `theata`, ideally to `elevation_deg` and `azimuth_deg`, since that's what they now mean.

**`C++ Sim/src/main.cpp`: improved.**

- Exit codes and stderr are right. `Error Output: boom` from a stub engine reached the UI correctly.
- Check the read itself, and validate the other inputs:

  ```cpp
  if (!(configFile >> v0 >> theata >> phi >> dt >> total_time)
      || v0 <= 0 || dt <= 0 || total_time <= 0) { /* stderr, return 1 */ }
  ```

- The `else` around the open check can become an early return.

**`Python Code/run_simulation.py`: clear and well organised.**

- With the DataFrame stored, the `sim_run` flag can go.
- `use_container_width` still warns on every render. Use `width="stretch"`.
- Paths still depend on the working directory.
- Replace the "another tip from Claude" comment with the reason for the line.

**Project housekeeping, all still open:**

- The README run command still points at `Python Code/src/`, which doesn't exist.
- The README still says Euler, but the update is now exact.
- There's no `requirements.txt`.
- `config.txt`, `trajectory.csv` and `.idea/` are still tracked.
- None of this work was committed at the time of review.

## Next steps

**Do this first: bugs 1–6.** On the scratch copy with these fixes, the following behaved correctly:

- Session A keeps its own shot.
- A missing binary shows a clean error and keeps the last plot.
- `v0=100` warns "Max flight time reached".
- `T=-1` and θ=0 show "No flight".

The scratch copy did not include the `min_value` on Max Flight Time.

**Then: unit tests before the CLI migration.** The migration rewrites `main.cpp` and `Simulation.cpp`, the same code that was just fixed, so those fixes need protecting first.

1. Move the physics into a CMake library target.
2. Change `runIntegration` to return a `std::vector<State>`. Tests need this, and so does the stdout migration, so it only has to be done once.
3. Add doctest or Catch2 with CTest, covering:
   - apex and flight time against the analytic values
   - range within one step
   - the same apex at all azimuths
   - the loop always terminating
   - row count for `dt=0.001, T=1`, which fails today and is a good first bug to fix with a test

**After that: CLI args and stdout.** This removes the remaining race, the 234 MB leftover file and the path problems.

**Limits of this review:** `cmake` wasn't installed in the review environment, so the code was built with `clang++` directly. The UI was driven through `AppTest`, not a real browser. The race numbers aren't comparable with the first review, because the test setup was different.

---

# First review

## Overall grade: C

The structure is sound for a ~140-line project: a clean split between languages, a working end-to-end pipeline and a good README. The grade is held back because **the simulator gives wrong answers**. Gravity is half its real value, the azimuth control doesn't work, and the app reports success when a run failed. There are also no tests, which is why the default settings hid all of this.

The two physics fixes are about 5 lines. With those and input validation, this is a solid B.

A scratch copy was compiled and the real Streamlit script was run headlessly, so these results are measured unless noted.

## C++ backend

### Critical bugs

1. **Gravity is halved (`C++ Sim/src/CannonBall.cpp:24`).** `vy + 0.5*gravity*dt` looks like a mix-up with the kinematic formula, where the `0.5` belongs in the position term.
   - The measured gravity from the output is **4.906 m/s²**.
   - At 45° and 50 m/s the range is 509.8 m, but the correct value is 254.8 m.
   - The committed `trajectory.csv` ends at t=10 s with the ball **108.5 m in the air**. The correct flight time is 7.21 s.

2. **The axes disagree (`C++ Sim/src/CannonBall.cpp:14-16`).** The launch maths treats Z as vertical, but gravity acts on Y. Only φ=90 works, and that's the default, so it stayed hidden:

| θ, φ | Rows | Max height | Expected with a real azimuth |
|---|---|---|---|
| 45, 90 | 1443 | 127.6 m | Correct shape, apart from bug 1 |
| 45, 45 | 1021 | 63.8 m | Same height, different direction |
| 45, 0 or 180 | 2 | 0 m | Full flight |
| 45, 225, 270 or 360 | 1 | 0 m | Full flight |

Azimuth should only rotate the shot, not change its height. Roughly half the slider range currently fires into the ground.

**Fix for both bugs** (the default shot keeps the same direction):

```cpp
// constructor: theta = elevation, phi = azimuth, Y is up
vx = vi * cos(el) * cos(az);
vy = vi * sin(el);
vz = vi * cos(el) * sin(az);

// update
y += vy*dt - 0.5*g*dt*dt;
vy -= g*dt;
```

This update is exact for constant gravity, so it is no longer Euler. If the assignment requires Euler, keep the existing order and use `vy -= g*dt`.

### Other bugs

3. **`dt=0` never terminates (`C++ Sim/src/Simulation.cpp:13`).** It writes about 17 MB/s to the CSV until it is killed or the disk fills.
4. **Bad config is accepted (`C++ Sim/src/main.cpp:8`).** The read is never checked:
   - `50 45 90 abc 10` prints "loaded params", sets `dt` to 0 and hangs.
   - An empty or short file silently uses defaults and still says "loaded".
   - A missing file also runs on defaults and exits 0, so the user's inputs are ignored.
5. **Write failures are ignored (`C++ Sim/src/Simulation.cpp:10,19`).** With a read-only CSV it still prints "Success" and exits 0.
6. **Time drifts because `currentTime += dt` accumulates error.** `dt=0.001, T=1` gives 1000 rows instead of 1001. Use `t = i*dt` with an integer counter.
7. **There is no ground impact point.** The last row is the step before landing, up to about 0.35 m short at `dt=0.01`. Interpolate to y=0.
8. **CSV output keeps only 6 significant digits.** In a long run, 1.44M rows had only 1.04M distinct times. Set `std::setprecision(17)` or similar.

### Design and modern C++

- **Encapsulation:** `CannonBall` has all-public state, and `Simulation` is a stateless class mixing physics with file output. Have it return a `std::vector<State>` and write the file elsewhere, which also makes it testable.
- **Cleanup:**
  - Fix the `theata` typo.
  - Use a constructor initializer list.
  - Make `pi` and gravity `constexpr` (`std::numbers::pi` needs C++20).
  - Put `toRadians` in an anonymous namespace, which is the only strict-warning hit.
  - Move the `CannonBall.h` include out of `Simulation.h`.
- **Memory safety:** good. There's no manual heap use, and ASan/UBSan were clean on the two configs run.

### CMake

Fine for this size, but dated.

- Use `target_include_directories` and add warning flags.
- Set `CMAKE_CXX_EXTENSIONS OFF` and a default build type.
- Split the physics into a library so tests can link to it.
- `cmake` wasn't installed in the review environment, so this file was reviewed by reading only, and the code was compiled with `clang++` directly.

## Python frontend

| Scenario | What the app did |
|---|---|
| Default shot, ball still 108 m up | "Target hit!" |
| φ=270, one row of data | "Target hit!" |
| Engine can't write, v0=999 | "Target hit!" showing **old data** |
| Binary not executable | Uncaught `PermissionError` traceback |
| Any widget changed after firing | Plot and table disappear |

- **`dt` is one click from the hang (`Python Code/run_simulation.py:15`).** It has no `min_value`, and its step of 0.01 equals its default. One click on "−" gives 0, and `subprocess.run` has no timeout, so the app would hang. The widget settings and the engine hang were confirmed separately, not the full click in a browser.
- **Stale data:** `os.path.exists` can't tell a new CSV from an old one, and one is committed to git. Delete it before each run, or stop using files.
- **Vanishing results:** output lives inside `if st.button`, so store it in `st.session_state`.
- **Errors:** catch `OSError` and `subprocess.TimeoutExpired`, and handle empty data. The C++ side prints errors to stdout while Python only shows stderr, so its message would never appear.
- **Paths:** they depend on the working directory. The stray `cmake-build-debug/trajectory.csv` is evidence of this. Build them from `Path(__file__)`.
- **3D plot:**
  - The axes scale independently, so the default shot shows an X axis of about 1e-14 from floating-point noise. Use `set_box_aspect` with shared limits.
  - Plotting `(x, z, y)` is fine. An earlier version of this review wrongly said it would make azimuth look reversed.
  - A ground plane and a landing marker would help.
- **Matplotlib:** a figure leak was expected but not found: 0 open after 25 runs, because Streamlit's runner calls `plt.close("all")`. Still prefer `matplotlib.figure.Figure`, because pyplot's state is global and sessions run in threads.
- **Pandas:** fine at this size. Use it for flight time, apex and range via `st.metric`, and downsample very small `dt` runs.
- **Deprecation:** `use_container_width` warns on every render on the installed Streamlit 1.67.0, and its stated removal date has passed. Use `width="stretch"`.

## Architecture and IPC

**Performance is fine.** A full engine run takes about 3.5 ms including process spawn, `read_csv` 0.5 ms and rendering 28 ms (measured on the local disk, not the USB drive). File I/O is not the bottleneck.

**Correctness is the real problem:**

- **Shared fixed filenames:** two sessions in a tight loop over 600 runs gave only **92 correct results**. Another 448 showed the other session's trajectory, and 60 silently fell back to defaults after reading a half-written config. This is a worst case, but two open tabs can really hit it.
- **No run identity:** nothing ties an output to its input, which is what makes the stale-data bug possible.
- **Weak failure signalling:** exit code 0 currently means nothing.
- **No schema:** both languages must agree on field order by convention.

This design is acceptable for a single-user demo, but it isn't safe with more than one session.

## Actionable improvements

### Quick refactors, in priority order

1. Fix gravity and the launch vector.
2. Validate input on both sides: `min_value` on `dt`, plus a checked read in C++ that rejects `dt <= 0`.
3. Return non-zero with a message on stderr for bad config or a failed write.
4. Add `timeout=` to `subprocess.run`, and cap the row count in C++.
5. Only report success if the ball landed, and say "max time reached" otherwise.
6. Fix the README run command: `Python Code/src/run_simulation.py` doesn't exist, because the file is in `Python Code/`.
7. Add a pinned `requirements.txt`.
8. Stop tracking `trajectory.csv`, `config.txt` and `.idea/`.
9. Add `session_state`, script-relative paths, integer time steps, impact interpolation and CSV precision.

### Advanced upgrades, in priority order

1. **Add tests and CI.** Check against the analytic range and flight time, and check that azimuth preserves height. Either check would have caught both critical bugs.
2. **Replace the files with CLI args in and CSV on stdout.** This is about 20 lines and removes the race, the stale data and the path problems together.
3. **Add air drag, then RK4.** Without drag, RK4 adds nothing because the exact update is already exact. Range error against the analytic answer:

   | Method | `dt=0.1` | `dt=0.01` | `dt=0.001` |
   |---|---|---|---|
   | Current code | +258 m | +255 m | +255 m |
   | Explicit Euler | +3.5 m | +0.35 m | +0.035 m |
   | Semi-implicit Euler | −3.5 m | −0.35 m | −0.035 m |
   | Exact update | −0.004 m | −0.0001 m | ~0 |

   These figures include impact interpolation. Semi-implicit Euler is no more accurate here, so only switch for its better stability once drag is in.

4. **Use pybind11 or nanobind** for a tighter integration. Calling C++ directly removes process and serialization overhead, and it's a good portfolio piece.
5. **Use Plotly** for a 3D plot that can be rotated, which matters more to users than any IPC change.

### On the two suggested upgrades

- **Sockets:** skip them. They add connection handling and a server lifecycle to save a fraction of a 3.5 ms step, for a job that runs once and exits.
- **JSON:** wait until there are nested or optional parameters, such as drag and mass. Five numbers fit in CLI args, and JSON doesn't replace validation, which is the actual gap.
