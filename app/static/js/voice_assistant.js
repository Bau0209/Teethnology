document.addEventListener('DOMContentLoaded', function () {
    const micButton = document.querySelector(".voice-assistant button");

    micButton.addEventListener("click", () => {
        console.log("🎤 Mic button clicked");
        startVoiceAssistant();
    });

    function startVoiceAssistant() {
        if (!('webkitSpeechRecognition' in window)) {
            alert("Your browser doesn't support speech recognition");
            return;
        }

        const recognition = new webkitSpeechRecognition();
        recognition.lang = 'en-US';
        recognition.interimResults = false;
        recognition.start();
        console.log("🎙️ Listening...");

        recognition.onresult = function (event) {
            const transcript = event.results[0][0].transcript;
            console.log("✅ Heard:", transcript);

            fetch('/dashboard/voice-assistant', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ query: transcript })
            })
                .then(response => {
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    let parsed = data.response; // already JSON object
                    console.log("📦 Parsed AI JSON:", parsed);

                    handleIntent(parsed);
                })
                .catch(err => {
                    console.error("❌ Fetch error:", err);
                    alert("Error talking to AI: " + err.message);
                });
        };

        recognition.onerror = function (event) {
            console.error("❌ Speech error:", event.error);
            alert("Speech error: " + event.error);
        };

        recognition.onend = function () {
            console.log("🛑 Speech recognition stopped");
        };
    }

    function speakOutput(output) {
        if (!output) return;

        const utterance = new SpeechSynthesisUtterance(output);

        // Voice Configuration
        const voices = speechSynthesis.getVoices();
        utterance.voice = voices.find(v => v.name.includes("Female")) || voices[0];
        utterance.lang = "en-GB";  // You can switch to "en-US", "fil-PH", etc.
        utterance.pitch = 1;       // 0 to 2
        utterance.rate = 0.9;      // 0.1 to 10
        utterance.volume = 1;      // 0 to 1

        speechSynthesis.speak(utterance);
    }


    function handleIntent(parsed) {
        const intent = parsed.intent;
        const target = parsed.target || {};
        const output = parsed.output || "";
        const currentYear = new Date().getFullYear();
        const selectedYear = target.year || currentYear;

        console.log("🎯 Intent:", intent, "target:", target);

        switch (intent) {
            case "SHOW_HOME":
                if (window.userContext.accessLevel === "owner") {
                    window.location.href = "/dashboard/owner_home?branch=all";
                } else if (window.userContext.accessLevel === "staff") {
                    window.location.href = `/dashboard/staff_home?branch=${window.userContext.accessBranch}`;
                }
                
                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_BRANCH_LIST":
                if (window.userContext.accessLevel === "owner") {
                    window.location.href = "/dashboard/branches";
                }
                else {
                    alert("You dont have permission to view that page: ");
                    console.warn("No Permission to:", intent);
                }
                
                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_BRANCH_DETAIL":
                if (target.branchName) {
                    console.log(target.branchName)
                    fetch("/dashboard/api/branch_lookup", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({ branchName: target.branchName })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.branch_id) {
                            window.location.href = `/dashboard/branch_info/${data.branch_id}`;
                        } else {
                            alert(data.error || "Branch not found");
                        }
                    })
                    .catch(err => {
                        console.error("Lookup error:", err);
                        alert("Error looking up branch");
                    });
                } else {
                    alert("Missing branchName");
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_APPOINTMENT_CALENDAR":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = "/dashboard/appointments?branch=all";
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/appointments?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = "/dashboard/appointments?branch=all";
                        });
                    } else {
                        console.log("No branch name. Showing all branch calendar");
                        window.location.href = "/dashboard/appointments?branch=all";
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/appointments?branch=${branchId}`;
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_APPOINTMENT_REQUEST":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = "/dashboard/appointment_req?branch=all";
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/appointment_req?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = "/dashboard/appointment_req?branch=all";
                        });
                    } else {
                        console.log("No branch name. Showing all branch calendar");
                        window.location.href = "/dashboard/appointment_req?branch=all";
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/appointment_req?branch=${branchId}`;
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_APPOINTMENT_ARCHIVES":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = "/dashboard/appointment_archives?branch=all";
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/appointment_archives?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = "/dashboard/appointment_archives?branch=all";
                        });
                    } else {
                        console.log("No branch name. Showing all branch calendar");
                        window.location.href = "/dashboard/appointment_archives?branch=all";
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/appointment_archives?branch=${branchId}`;
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_PATIENT_LIST":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = "/dashboard/patients?branch=all";
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/patients?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = "/dashboard/patients?branch=all";
                        });
                    } else {
                        console.log("No branch name. Showing all branch calendar");
                        window.location.href = "/dashboard/patients?branch=all";
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/patients?branch=${branchId}`;
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_PATIENT_DETAILS":
                if (target.firstName || target.lastName) {
                    // Call the fuzzy-matching patient lookup API
                    fetch("/dashboard/api/patient_lookup", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            firstName: target.firstName || "",
                            middleName: target.middleName || "",
                            lastName: target.lastName || ""
                        })
                    })
                    .then(async res => {
                        const data = await res.json();

                        if (!res.ok) {
                            // Handle error messages
                            console.warn("Lookup failed:", data.message || data.error);
                            speakOutput(data.message || "I couldn't find that patient.");
                            return;
                        }

                        if (data.patient_id) {
                            const patientId = data.patient_id;
                            window.location.href = `/dashboard/patient_info/${patientId}`;
                            speakOutput(output);
                        } else {
                            console.log("Can't find patient");
                            speakOutput("I couldn't find that patient.");
                        }
                    })
                    .catch(err => {
                        console.error("Patient lookup failed:", err);
                        speakOutput("Something went wrong looking up the patient.");
                    });

                    if (output) {
                        speakOutput(output);
                    }
                } else {
                    console.log("❌ No patient name provided.");
                    speakOutput("Please tell me the patient's full name so I can find the record.");
                }
                break;

            case "SHOW_PATIENT_PROCEDURES":
                if (target.firstName || target.lastName) {
                    // Call the fuzzy-matching patient lookup API
                    fetch("/dashboard/api/patient_lookup", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            firstName: target.firstName || "",
                            middleName: target.middleName || "",
                            lastName: target.lastName || ""
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.error || (data.message && data.message.includes("Can't find"))) {
                        } else if (data.patient_id) {
                            const patientId = data.patient_id;
                            window.location.href = `/dashboard/patient_procedure/${patientId}`;
                            
                        } else {
                            console.log("Can't find patient");
                        }
                    })
                    .catch(err => {
                        console.error("Patient lookup failed:", err);
                    });

                    if (output) {
                        speakOutput(output);
                    }
                }
                break;

            case "SHOW_PATIENT_DENTAL_RECORDS":
                if (target.firstName || target.lastName) {
                    // Call the fuzzy-matching patient lookup API
                    fetch("/dashboard/api/patient_lookup", {
                        method: "POST",
                        headers: {
                            "Content-Type": "application/json"
                        },
                        body: JSON.stringify({
                            firstName: target.firstName || "",
                            middleName: target.middleName || "",
                            lastName: target.lastName || ""
                        })
                    })
                    .then(res => res.json())
                    .then(data => {
                        if (data.error || (data.message && data.message.includes("Can't find"))) {
                        } else if (data.patient_id) {
                            const patientId = data.patient_id;
                            window.location.href = `/dashboard/patient_dental_rec/${patientId}`;
                            
                        } else {
                            console.log("Can't find patient");
                        }
                    })
                    .catch(err => {
                        console.error("Patient lookup failed:", err);
                    });

                    if (output) {
                        speakOutput(output);
                    }
                }
                break;

            case "SHOW_EMPLOYEE_LIST":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = "/dashboard/employees?branch=all";
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/employees?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = "/dashboard/employees?branch=all";
                        });
                    } else {
                        console.log("No branch name. Showing all branch calendar");
                        window.location.href = "/dashboard/employees?branch=all";
                    }
                } else {
                    alert("You dont have permission to view that page: ");
                    console.warn("No Permission to:", intent);
                }
                
                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_INVENTORY_LIST":
                if (target.category) {
                    // If category is provided, choose the correct inventory route
                    let route = "/dashboard/inventory"; // default overall

                    switch (target.category.toLowerCase()) {
                        case "consumable":
                        case "consumables":
                            route = "/dashboard/inventory_consumable";
                            break;

                        case "equipment":
                        case "equipments":
                            route = "/dashboard/inventory_equipment";
                            break;

                        case "sterilization":
                        case "sterilizations":
                            route = "/dashboard/inventory_sterilization";
                            break;

                        case "lab material":
                        case "lab materials":
                        case "lab":
                            route = "/dashboard/inventory_lab_material";
                            break;

                        case "medication":
                        case "medications":
                            route = "/dashboard/inventory_medication";
                            break;

                        default:
                            route = "/dashboard/inventory"; // fallback to overall
                    }

                    // Handle branch filter if available
                    if (target.branchName) {
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = `${route}?branch=all`;
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `${route}?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = `${route}?branch=all`;
                        });
                    } else {
                        console.log("No branch name. Showing all branches");
                        window.location.href = `${route}?branch=all`;
                    }

                } else {
                    // If no category provided, just fallback to overall inventory
                    if (target.branchName) {
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = "/dashboard/inventory?branch=all";
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/inventory?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = "/dashboard/inventory?branch=all";
                        });
                    } else {
                        console.log("No branch name. Showing all branches");
                        window.location.href = "/dashboard/inventory?branch=all";
                    }
                }


            console.log("Output:", output);
            if (output) {
                speakOutput(output);
            }
            break;                

            case "SHOW_TRANSACTION_LIST":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = "/dashboard/transactions?branch=all";
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/transactions?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = "/dashboard/transactions?branch=all";
                        });
                    } else {
                        console.log("No branch name. Showing all branch calendar");
                        window.location.href = "/dashboard/transactions?branch=all";
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/transactions?branch=${branchId}`;
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_TRANSACTION_FILTERED":
                let urlT = `/dashboard/transactions_filtered?`;
                if (target.patientName) urlT += `patient=${encodeURIComponent(target.patientName)}&`;
                if (target.date) urlT += `date=${encodeURIComponent(target.date)}&`;
                if (target.procedure) urlT += `procedure=${encodeURIComponent(target.procedure)}&`;
                window.location.href = urlT.slice(0, -1);
                break;

            case "SHOW_BALANCE_RECORD_LIST":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("can't find branch. show all data");
                                window.location.href = "/dashboard/balance_record?branch=all";
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/balance_record?branch=${branchId}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = "/dashboard/balance_record?branch=all";
                        });
                    } else {
                        console.log("No branch name. Showing all branch calendar");
                        window.location.href = "/dashboard/balance_record?branch=all";
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/balance_record?branch=${branchId}`;
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_BALANCE_RECORD_FILTERED":
                if (target.patientName) {
                    window.location.href = `/dashboard/balance_filtered?patient=${encodeURIComponent(target.patientName)}`;
                } else {
                    alert("Missing patientName");
                }
                break;

            case "SHOW_REVENUE_REPORTS": 
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("Can't find branch. Show all data");
                                window.location.href = `/dashboard/reports?branch=all&selected_year=${selectedYear}`;
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/reports?branch=${branchId}&selected_year=${selectedYear}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = `/dashboard/reports?branch=all&selected_year=${selectedYear}`;
                        });
                    } else {
                        console.log("No branch name. Showing all branch reports");
                        window.location.href = `/dashboard/reports?branch=all&selected_year=${selectedYear}`;
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    // Staff limited to their branch
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/reports?branch=${branchId}&selected_year=${selectedYear}`;
                } else {
                    alert("You don't have permission to view that page.");
                    console.warn("No Permission to:", intent);
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_PATIENT_APPOINTMENTS_REPORTS":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("Can't find branch. Show all data");
                                window.location.href = `/dashboard/report_patients?branch=all&selected_year=${selectedYear}`;
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/report_patients?branch=${branchId}&selected_year=${selectedYear}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = `/dashboard/report_patients?branch=all&selected_year=${selectedYear}`;
                        });
                    } else {
                        console.log("No branch name. Showing all branch reports");
                        window.location.href = `/dashboard/report_patients?branch=all&selected_year=${selectedYear}`;
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    // Staff limited to their branch
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/report_patients?branch=${branchId}&selected_year=${selectedYear}`;
                } else {
                    alert("You don't have permission to view that page.");
                    console.warn("No Permission to:", intent);
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_MARKETING_REPORTS":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("Can't find branch. Show all data");
                                window.location.href = `/dashboard/report_marketing?branch=all&selected_year=${selectedYear}`;
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/report_marketing?branch=${branchId}&selected_year=${selectedYear}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = `/dashboard/report_marketing?branch=all&selected_year=${selectedYear}`;
                        });
                    } else {
                        console.log("No branch name. Showing all branch reports");
                        window.location.href = `/dashboard/report_marketing?branch=all&selected_year=${selectedYear}`;
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    // Staff limited to their branch
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/report_marketing?branch=${branchId}&selected_year=${selectedYear}`;
                } else {
                    alert("You don't have permission to view that page.");
                    console.warn("No Permission to:", intent);
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_INVENTORY_REPORTS":
                if (window.userContext.accessLevel === "owner") {
                    if (target.branchName) {
                        // Call the fuzzy-matching branch lookup API
                        fetch("/dashboard/api/branch_lookup", {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json"
                            },
                            body: JSON.stringify({ branchName: target.branchName })
                        })
                        .then(res => res.json())
                        .then(data => {
                            if (data.error) {
                                console.log("Can't find branch. Show all data");
                                window.location.href = `/dashboard/report_inventory?branch=all&selected_year=${selectedYear}`;
                            } else {
                                const branchId = data.branch_id;
                                window.location.href = `/dashboard/report_inventory?branch=${branchId}&selected_year=${selectedYear}`;
                            }
                        })
                        .catch(err => {
                            console.error("Branch lookup failed:", err);
                            window.location.href = `/dashboard/report_inventory?branch=all&selected_year=${selectedYear}`;
                        });
                    } else {
                        console.log("No branch name. Showing all branch reports");
                        window.location.href = `/dashboard/report_inventory?branch=all&selected_year=${selectedYear}`;
                    }
                } else if (window.userContext.accessLevel === "staff") {
                    // Staff limited to their branch
                    const branchId = window.userContext.accessBranch;
                    window.location.href = `/dashboard/report_inventory?branch=${branchId}&selected_year=${selectedYear}`;
                } else {
                    alert("You don't have permission to view that page.");
                    console.warn("No Permission to:", intent);
                }

                console.log("Output:", output);
                if (output) {
                    speakOutput(output);
                }
                break;

            case "SHOW_DATABASE_DATA":
                if (target.table) {
                    let urlD = `/dashboard/database?table=${encodeURIComponent(target.table)}`;
                    if (target.query) urlD += `&query=${encodeURIComponent(target.query)}`;
                    window.location.href = urlD;
                } else {
                    alert("Missing table name");
                }
                break;
            
            case "ANSWER_WITHOUT_CONTEXT":
                console.log("Output:", output);

                if (output) {
                    speakOutput(output);
                }
                break;

            default:
                if (output) {
                    speakOutput(output);
                }
                alert("AI gave unknown intent: " + intent);
                console.warn("Unknown intent:", parsed);
        }
    }
});
