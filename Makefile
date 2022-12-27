TARGET = cpass
CC = gcc

CFLAGS = -Wall -Wextra -std=c99 -O3 -DSQLITE_HAS_CODEC
CFLAGS += -iquote $(INC_DIR) -I lib/sqlcipher -lsqlcipher
CFLAGS += -MMD -MP

DFLAGS = -DSQLITE_HAS_CODEC

LDFLAGS = -L lib -lssl -lcrypto -lsqlite3 -lncurses

SRC_DIR = src
BUILD_DIR = build
INC_DIR = includes

OBJ_DIR = $(BUILD_DIR)
DEP_DIR = $(BUILD_DIR)

vpath %.c $(SRC_DIR) $(SRC_DIR)/db
vpath %.h $(INC_DIR) $(INC_DIR)/cpass

vpath %.o $(OBJ_DIR)
vpath %.d $(DEP_DIR)

SRC := main.c

OBJ := $(SRC:%.c=$(OBJ_DIR)/%.o)
DEP := $(OBJ:.o=.d)

ifneq ($(shell tput colors),0)
    BOLD = \e[1m
    RESET = \033[00m
    BLUE = \e[34m
    RED = \e[31m
    CYAN = \e[36m
endif

ECHO = /bin/echo -e
DIE = exit 1

ECHO_OK = @ $(ECHO) "$(BOLD)[$(BLUE)OK$(RESET)$(BOLD)]$(RESET)"
ECHO_KO = @ $(ECHO) "$(BOLD)[$(RED)KO$(RESET)$(BOLD)]$(RESET)"

all: $(TARGET)
	@ $(ECHO) "$(BOLD)Nothing to do.$(RESET)"

%.c:
	$(ECHO_KO) "Missing file: $@" && $(DIE)

%:
	$(ECHO_KO) "Unknown directive $@" && $(DIE)

$(TARGET): $(OBJ)
	$(ECHO_OK) "Linking $(CYAN)$(notdir $?)$(RESET)$(BOLD)...$(RESET)"
	@ $(CC) $(CFLAGS) $^ -o $@ $(LDFLAGS)
	$(ECHO_OK) "Linked $(BLUE)$(shell echo "$?" | wc -w)$(RESET) file(s)"

-include $(DEP)

$(BUILD_DIR)/%.o: %.c
	@ mkdir -p $(@D)
	@ $(CC) $(CFLAGS) -c $< -o $@ || $(DIE)
	$(ECHO_OK) "Compiled $(CYAN)$<$(RESET)"

$(BUILD_DIR)/%.d: %.c
	@ mkdir -p $(@D)
	@ $(CC) $(CFLAGS) -MM -MT $(@:.d=.o) $< -MF $@

clean:
	@ $(RM) -r "$(BUILD_DIR)"
	$(ECHO_OK) "Deleted $(BLUE)$(BUILD_DIR)$(RESET)"

fclean: clean
	@ $(RM) "$(TARGET)"
	$(ECHO_OK) "Deleted $(BLUE)$(TARGET)$(RESET)"

re: fclean all

.PHONY: clean fclean re
