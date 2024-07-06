ASS_DIR := ./assets
EXP_DIR := ./exports
LOG_DIR := ./logs
OUT_DIR := ./out

.PHONY: all clean

all: $(ASS_DIR) $(EXP_DIR) $(LOG_DIR) $(OUT_DIR)

$(ASS_DIR) $(EXP_DIR) $(LOG_DIR) $(OUT_DIR):
	mkdir -p $@

clean:
	rm -rf $(EXP_DIR) $(LOG_DIR) $(OUT_DIR)
