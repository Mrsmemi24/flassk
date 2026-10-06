(() => {
    const form = document.querySelector("#device-form");
    if (!form) return;

    const vlanList = document.querySelector("#vlan-list");
    const vlanTemplate = document.querySelector("#vlan-template");
    const formMessage = document.querySelector("#form-message");
    const addVlanButton = document.querySelector("#add-vlan");
    const maxVlans = 64;
    const allowedProtocols = ["OSPF", "BGP", "STP", "LACP", "IPSec", "NAT", "RIP", "EIGRP", "VTP", "CAPWAP", "HA", "LLDP", "802.11X"];
    const allowedPolicies = ["ALLOW_ALL", "BLOCK_ALL", "BLOCK_IP", "REQUIRED_IP", "RESTRICT_SSH"];
    const protocolsByKey = new Map(allowedProtocols.map((value) => [value.toUpperCase(), value]));
    const policiesByKey = new Map(allowedPolicies.map((value) => [value.toUpperCase(), value]));
    const ipv4Octet = "(?:25[0-5]|2[0-4]\\d|1\\d\\d|[1-9]?\\d)";
    const ipv4Pattern = new RegExp(`^(?:${ipv4Octet}\\.){3}${ipv4Octet}$`);
    const macPattern = /^(?:[0-9a-f]{2}:){4,5}[0-9a-f]{2}$/i;
    const namePattern = /^\p{L}[\p{L}\p{M}\p{N} .,'()/_-]{0,79}$/u;
    const portPattern = /^(?:(?:GigabitEthernet|FastEthernet|TenGigabitEthernet|Ethernet)\d+(?:\/\d+){1,2}|WLAN\d+)$/i;

    function splitValues(value) {
        return value.split(",").map((item) => item.trim()).filter(Boolean);
    }

    function showError(input, message) {
        input.classList.toggle("is-invalid", Boolean(message));
        if (message) input.setAttribute("aria-invalid", "true");
        else input.removeAttribute("aria-invalid");
        const card = input.closest("[data-vlan-card]");
        const error = card
            ? input.closest(".field").querySelector("[data-error]")
            : document.querySelector(`[data-error-for="${input.dataset.field}"]`);
        if (error) error.textContent = message || "";
    }

    function clearErrors() {
        form.querySelectorAll(".is-invalid").forEach((input) => showError(input, ""));
        formMessage.textContent = "";
    }

    function showServerError(result) {
        const field = result.field || "form";
        if (field.startsWith("vlan:")) {
            const [, vlanId, inputName] = field.split(":");
            const card = [...vlanList.querySelectorAll("[data-vlan-card]")].find((candidate) => {
                const numericId = candidate.querySelector('[data-field="id"]').value;
                return `VL${Number(numericId)}` === vlanId;
            });
            const input = card?.querySelector(`[data-field="${inputName}"]`);
            if (input) showError(input, result.error);
            else formMessage.textContent = result.error;
            input?.focus();
            return;
        }
        const input = field === "vlan_id"
            ? vlanList.querySelector('[data-field="id"]')
            : form.querySelector(`[data-field="${field}"]`);
        if (input) {
            showError(input, result.error);
            input.focus();
        } else {
            formMessage.textContent = result.error || "The device could not be saved.";
        }
    }

    function updateVlanCards() {
        const cards = [...vlanList.querySelectorAll("[data-vlan-card]")];
        cards.forEach((card, index) => {
            card.querySelector("[data-vlan-number]").textContent = index + 1;
            card.querySelector("[data-remove-vlan]").disabled = cards.length === 1;
            const idInput = card.querySelector('[data-field="id"]');
            const inputId = `vlan-${index + 1}-id`;
            idInput.id = inputId;
            idInput.closest(".field").querySelector("label").htmlFor = inputId;
            const idError = idInput.closest(".field").querySelector("[data-error]");
            idError.id = `error-vlan-id-${index + 1}`;
            idInput.setAttribute("aria-describedby", idError.id);
            ["IP", "Ports", "Policies"].forEach((field) => {
                const input = card.querySelector(`[data-field="${field}"]`);
                const fieldId = `vlan-${index + 1}-${field.toLowerCase()}`;
                input.id = fieldId;
                input.closest(".field").querySelector("label").htmlFor = fieldId;
                const error = input.closest(".field").querySelector("[data-error]");
                error.id = `error-vlan-${field.toLowerCase()}-${index + 1}`;
                input.setAttribute("aria-describedby", error.id);
            });
        });
        addVlanButton.disabled = cards.length >= maxVlans;
    }

    function validateForm() {
        clearErrors();
        let firstInvalid = null;
        const fail = (input, message) => {
            showError(input, message);
            firstInvalid ||= input;
        };

        const identifier = form.querySelector('[data-field="identifier"]');
        if (!identifier.readOnly && !macPattern.test(identifier.value.trim())) {
            fail(identifier, "Enter a valid colon-separated MAC address.");
        }

        const name = form.querySelector('[data-field="name"]');
        if (!namePattern.test(name.value.trim())) fail(name, "Start with a letter and use valid text characters only.");

        const deviceIp = form.querySelector('[data-field="device_ip"]');
        if (!ipv4Pattern.test(deviceIp.value.trim())) fail(deviceIp, "Enter a complete IPv4 address from 0.0.0.0 to 255.255.255.255.");

        const status = form.querySelector('[data-field="status"]');
        if (!["online", "offline"].includes(status.value)) fail(status, "Choose online or offline.");

        const protocols = splitValues(form.querySelector('[data-field="protocols"]').value);
        const protocolInput = form.querySelector('[data-field="protocols"]');
        if (!protocols.length || protocols.some((value) => !protocolsByKey.has(value.toUpperCase()))) {
            fail(protocolInput, `Use supported protocols only: ${allowedProtocols.join(", ")}.`);
        } else if (new Set(protocols.map((value) => value.toUpperCase())).size !== protocols.length) {
            fail(protocolInput, "Remove duplicate protocols.");
        }

        const cards = [...vlanList.querySelectorAll("[data-vlan-card]")];
        const seenIds = new Set();
        if (!cards.length || cards.length > maxVlans) formMessage.textContent = `Add between one and ${maxVlans} VLANs.`;
        for (const card of cards) {
            const idInput = card.querySelector('[data-field="id"]');
            const idValue = idInput.value.trim();
            const idNumber = Number(idValue);
            if (!/^\d+$/.test(idValue) || !Number.isInteger(idNumber) || idNumber < 1 || idNumber > 4094) {
                fail(idInput, "Enter a numeric VLAN ID from 1 to 4094.");
            } else if (seenIds.has(idNumber)) {
                fail(idInput, "Each VLAN ID must be unique.");
            } else {
                seenIds.add(idNumber);
            }

            const ipInput = card.querySelector('[data-field="IP"]');
            if (!ipv4Pattern.test(ipInput.value.trim())) fail(ipInput, "Enter a valid IPv4 address.");

            const portsInput = card.querySelector('[data-field="Ports"]');
            const ports = splitValues(portsInput.value);
            if (!ports.length || ports.some((value) => !portPattern.test(value))) {
                fail(portsInput, "Use interface names such as GigabitEthernet0/1 or WLAN0.");
            } else if (new Set(ports.map((value) => value.toLowerCase())).size !== ports.length) {
                fail(portsInput, "Remove duplicate ports.");
            }

            const policiesInput = card.querySelector('[data-field="Policies"]');
            const policies = splitValues(policiesInput.value);
            if (!policies.length || policies.some((value) => !policiesByKey.has(value.toUpperCase()))) {
                fail(policiesInput, `Use supported policies only: ${allowedPolicies.join(", ")}.`);
            } else if (new Set(policies.map((value) => value.toUpperCase())).size !== policies.length) {
                fail(policiesInput, "Remove duplicate policies.");
            }
        }

        firstInvalid?.focus();
        return !firstInvalid && !formMessage.textContent;
    }

    addVlanButton.addEventListener("click", () => {
        const usedIds = new Set([...vlanList.querySelectorAll('[data-field="id"]')].map((input) => Number(input.value)));
        let nextId = 1;
        while (usedIds.has(nextId) && nextId <= 4094) nextId += 1;
        if (nextId > 4094) {
            formMessage.textContent = "No unused VLAN IDs remain.";
            return;
        }
        const card = vlanTemplate.content.cloneNode(true);
        card.querySelector('[data-field="id"]').value = nextId;
        vlanList.append(card);
        updateVlanCards();
        vlanList.lastElementChild.querySelector('[data-field="IP"]').focus();
    });

    vlanList.addEventListener("click", (event) => {
        const removeButton = event.target.closest("[data-remove-vlan]");
        if (removeButton && vlanList.querySelectorAll("[data-vlan-card]").length > 1) {
            removeButton.closest("[data-vlan-card]").remove();
            updateVlanCards();
        }
    });

    form.addEventListener("input", (event) => {
        if (event.target.matches("input, select")) showError(event.target, "");
        formMessage.textContent = "";
    });

    form.addEventListener("submit", async (event) => {
        event.preventDefault();
        if (!validateForm()) return;

        const vlanRecords = {};
        for (const card of vlanList.querySelectorAll("[data-vlan-card]")) {
            const value = (field) => card.querySelector(`[data-field="${field}"]`).value.trim();
            const vlanId = `VL${Number(value("id"))}`;
            vlanRecords[vlanId] = {
                Ports: splitValues(value("Ports")),
                Policies: splitValues(value("Policies")).map((policy) => policiesByKey.get(policy.toUpperCase())),
                ET: card.querySelector('[data-field="ET"]').checked,
                IP: value("IP"),
                SSH: card.querySelector('[data-field="SSH"]').checked,
            };
        }

        const protocols = splitValues(form.querySelector('[data-field="protocols"]').value)
            .map((protocol) => protocolsByKey.get(protocol.toUpperCase()));
        const payload = {
            identifier: form.querySelector('[data-field="identifier"]').value.trim(),
            record: {
                Name: form.querySelector('[data-field="name"]').value.trim(),
                IP: form.querySelector('[data-field="device_ip"]').value.trim(),
                Protocolos: protocols,
                status: form.querySelector('[data-field="status"]').value,
                VLANs: vlanRecords,
            },
        };

        const submitButton = form.querySelector('[type="submit"]');
        submitButton.disabled = true;
        formMessage.textContent = "";
        try {
            const response = await fetch(form.action, {
                method: "POST",
                credentials: "same-origin",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": form.querySelector('[name="csrf_token"]').value,
                },
                body: JSON.stringify(payload),
            });
            if (response.redirected) {
                window.location.assign(response.url);
                return;
            }
            const result = await response.json();
            if (!response.ok) {
                showServerError(result);
                return;
            }
            window.location.assign(form.dataset.successUrl);
        } catch (error) {
            formMessage.textContent = "The server could not be reached. Check your connection and try again.";
        } finally {
            submitButton.disabled = false;
        }
    });

    updateVlanCards();
})();
