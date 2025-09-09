
document.addEventListener('DOMContentLoaded', function() {
    // Complete route mapping with parent-child relationships
    const routeMap = {
        // Home routes
        'owner_home': { name: 'Home', url: '{{ url_for("dashboard.owner_home") }}' },
        'staff_home': { name: 'Home', url: '{{ url_for("dashboard.staff_home") }}' },
        
        // Branches hierarchy
        'branches': { name: 'Branches', url: '{{ url_for("dashboard.branches") }}' },
        'branch_info': { name: 'Branch Info', parent: 'branches' },
        
        // Patients hierarchy
        'patients': { name: 'Patients', url: '{{ url_for("dashboard.patients") }}' },
        'patient_info': { name: 'Patient Info', parent: 'patients' },
        'procedure_history': { name: 'Procedure History', parent: 'patient_info' },
        'dental_record': { name: 'Dental Records', parent: 'procedure_history' },
        
        // Employees hierarchy
        'employees': { name: 'Employees', url: '{{ url_for("dashboard.employees") }}' },
        'basic_info': { name: 'Basic Info', parent: 'employees' },
        'work_details': { name: 'Work Details', parent: 'employees' },
        
        // Inventory hierarchy
        'inventory': { name: 'Inventory', url: '{{ url_for("dashboard.inventory") }}' },
        'consumable': { name: 'Consumable', parent: 'inventory' },
        'equipment': { name: 'Equipment', parent: 'inventory' },
        'sterilization': { name: 'Sterilization', parent: 'inventory' },
        'lab_materials': { name: 'Lab Materials', parent: 'inventory' },
        'medication': { name: 'Medication', parent: 'inventory' },
        
        // Reports hierarchy
        'reports': { name: 'Reports', url: '{{ url_for("dashboard.reports") }}' },
        'revenue': { name: 'Revenue', parent: 'reports' },
        'patients_report': { name: 'Patients', parent: 'reports' },
        'marketing': { name: 'Marketing', parent: 'reports' },
        'inventory_report': { name: 'Inventory', parent: 'reports' }
    };

    function updateBreadcrumbs() {
        const path = window.location.pathname.split('/').filter(segment => segment && segment !== 'dashboard');
        const breadcrumbContainer = document.getElementById('breadcrumb-container');
        
        let breadcrumbHtml = '';
        const homeUrl = '{{ url_for("dashboard.owner_home") if access_level == "owner" else url_for("dashboard.staff_home") }}';
        breadcrumbHtml += `<a href="${homeUrl}">Home</a>`;
        
        if (path.length > 0) {
            breadcrumbHtml += '<span class="separator">></span>';
        }
        
        // Track processed segments to handle dynamic IDs
        const processedSegments = [];
        
        path.forEach((segment, index) => {
            const isLast = index === path.length - 1;
            let routeInfo = routeMap[segment] || { 
                name: segment.replace(/_/g, ' ').replace(/(^|\s)\S/g, l => l.toUpperCase()),
                parent: processedSegments[processedSegments.length - 1] || null
            };
            
            // Handle numeric IDs (like patient/5)
            if (!isNaN(segment) && processedSegments.length > 0) {
                routeInfo = {
                    name: routeMap[processedSegments[processedSegments.length - 1]]?.name + ' Details',
                    parent: processedSegments[processedSegments.length - 1]
                };
            }
            
            processedSegments.push(segment);
            
            // Determine URL
            let segmentUrl;
            if (isLast) {
                segmentUrl = '#';
            } else if (routeInfo.url) {
                segmentUrl = routeInfo.url;
            } else if (routeInfo.parent) {
                const parentRoute = routeMap[routeInfo.parent] || { url: `/${routeInfo.parent}` };
                segmentUrl = parentRoute.url;
            } else {
                segmentUrl = homeUrl;
            }
            
            breadcrumbHtml += isLast 
                ? `<span class="current">${routeInfo.name}</span>`
                : `<a href="${segmentUrl}">${routeInfo.name}</a>`;
            
            if (!isLast && index < path.length - 1) {
                breadcrumbHtml += '<span class="separator">></span>';
            }
        });
        
        breadcrumbContainer.innerHTML = breadcrumbHtml;
    }

    // Initial load
    updateBreadcrumbs();
    
    // Update when navigating
    document.addEventListener('click', function(e) {
        if (e.target.closest('a') && !e.target.closest('a').hasAttribute('target')) {
            setTimeout(updateBreadcrumbs, 50);
        }
    });
});