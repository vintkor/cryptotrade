"use strict";


$(document).ready(function () {

    // =================================================== menu ===================================================

    var contentSections = $('.cd-section'),
        navigationItems = $('#main__nav a');

    updateNavigation();
    $(window).on('scroll', function () {
        updateNavigation();
    });

    //smooth scroll to the section
    navigationItems.on('click', function (event) {
        event.preventDefault();
        smoothScroll($(this.hash));
        $('#main__nav').removeClass('open');
    });

    //smooth scroll to second section
    // $('.cd-scroll-down').on('click', function(event){
    //     event.preventDefault();
    //     smoothScroll($(this.hash));
    // });

    //open-close navigation on touch devices
    $('.cd-nav-trigger').on('click', function () {
        $('#main__nav').toggleClass('open');

    });
    //close navigation on touch devices when selectin an elemnt from the list
    // $('.touch #main__nav a').on('click', function(){
    //     $('.touch #main__nav').removeClass('open');
    // });

    function updateNavigation() {
        contentSections.each(function () {
            var $this = $(this);
            var activeSection = $('#main__nav a[href="#' + $this.attr('id') + '"]').data('number') - 1;
            if (($this.offset().top - $(window).height() / 2 < $(window).scrollTop()) && ($this.offset().top + $this.height() - $(window).height() / 2 > $(window).scrollTop())) {
                navigationItems.eq(activeSection).addClass('is-selected');
            } else {
                navigationItems.eq(activeSection).removeClass('is-selected');
            }
        });

    }

    function smoothScroll(target) {
        $('body,html').stop().animate(
            {'scrollTop': target.offset().top - $('header').outerHeight()},
            900
        );
    }

    // =================================================== menu ===================================================


    // =================================================== select language ===================================================

    var x, i, j, selElmnt, a, b, c;
    /*look for any elements with the class "custom-select":*/
    x = document.getElementsByClassName("custom-select");
    for (i = 0; i < x.length; i++) {
        selElmnt = x[i].getElementsByTagName("select")[0];
        /*for each element, create a new DIV that will act as the selected item:*/
        a = document.createElement("DIV");
        a.setAttribute("class", "select-selected");
        a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
        x[i].appendChild(a);
        /*for each element, create a new DIV that will contain the option list:*/
        b = document.createElement("DIV");
        b.setAttribute("class", "select-items select-hide");
        for (j = 0; j < selElmnt.length; j++) {
            /*for each option in the original select element,



            create a new DIV that will act as an option item:*/
            c = document.createElement("a");
            c.setAttribute("href", selElmnt[j].getAttribute('data-url'));
            c.innerHTML = selElmnt.options[j].innerHTML;
            // c.setAttribute("data-language", selElmnt.options[j].innerHTML);
            c.addEventListener("click", function (e) {
                $('.select-selected').css('display', 'none');
                /*when an item is clicked, update the original select box,
                and the selected item:*/
                var y, i, k, s, h;
                s = this.parentNode.parentNode.getElementsByTagName("select")[0];
                h = this.parentNode.previousSibling;
                for (i = 0; i < s.length; i++) {
                    if (s.options[i].innerHTML == this.innerHTML) {
                        s.selectedIndex = i;
                        h.innerHTML = this.innerHTML;
                        y = this.parentNode.getElementsByClassName("same-as-selected");
                        for (k = 0; k < y.length; k++) {
                            y[k].removeAttribute("class");
                        }
                        this.setAttribute("class", "same-as-selected");
                        h.setAttribute("data-language", i);
                        // this.setAttribute("href", $(i).data('url'));

                        break;
                    }
                }
                h.click();
            });
            b.appendChild(c);
        }
        x[i].appendChild(b);
        a.addEventListener("click", function (e) {
            /*when the select box is clicked, close any other select boxes,
            and open/close the current select box:*/
            e.stopPropagation();
            closeAllSelect(this);
            this.nextSibling.classList.toggle("select-hide");
            this.classList.toggle("select-arrow-active");
        });
    }

    function closeAllSelect(elmnt) {
        /*a function that will close all select boxes in the document,
        except the current select box:*/
        var x, y, i, arrNo = [];
        x = document.getElementsByClassName("select-items");
        y = document.getElementsByClassName("select-selected");
        for (i = 0; i < y.length; i++) {
            if (elmnt == y[i]) {
                arrNo.push(i)
            } else {
                y[i].classList.remove("select-arrow-active");
            }
        }
        for (i = 0; i < x.length; i++) {
            if (arrNo.indexOf(i)) {
                x[i].classList.add("select-hide");
            }
        }
    }

    /*if the user clicks anywhere outside the select box,
    then close all select boxes:*/
    document.addEventListener("click", closeAllSelect);

    // =================================================== select language ===================================================

    // =================================================== progressbar ===================================================
    // on page load...
    moveProgressBar($('.custom__progress-wrap'));
    // on browser resize...
    $(window).resize(function () {

        moveProgressBar($('.custom__progress-wrap'));

        $('.first-block').css('padding-top', $('header').outerHeight());

        $(document).on('click', '.team__item', function (e) {
            if ($(window).width() < 501) {

                $('body,html').stop().animate(
                    {'scrollTop': $('.team__human_all').offset().top - $('header').outerHeight()},
                    400
                );
                500
            }
        });

        //    team block resize

        if ($(window).width() < 769) {

            $('.team__big__wrapper').addClass('owl-theme owl-carousel team__big__wrapper-slider');

            humanSingle.css('display', 'block');

            $('.team__big__wrapper-slider').owlCarousel({
                items: 1,
                nav: true,
                arrows: true,
                margin: 0,
                dotsEach: true,
                dots: false,
                navText: ["<div class='arl'></div>", "<div class='arr'></div>"],
                mouseDrag: true,
                responsive: {
                    320: {
                        items: 1
                    },
                    769: {
                        items: 1
                    },
                    1200: {
                        items: 1
                    }
                }
            });
        } else {
            $('.team__big__wrapper-slider').owlCarousel('destroy');
            $('.team__big__wrapper').removeClass('owl-theme owl-carousel team__big__wrapper-slider');
            humanSingle.css('display', 'none');

            human.removeClass('active');
            humanSingle.css('display', 'none');

            var item = $('.owl-item.active').find('.team__player');

            item.first().addClass('active');

            $('.team__big[data-id="' + item.data('id') + '"]').css('display', 'block');

            getFieldCoordinates();


        }

        //    team block resize


    });

    // SIGNATURE PROGRESS
    function moveProgressBar(selector) {
        var getPercent = (selector.data('progress-percent') / 100);
        var getProgressWrapWidth = selector.width();
        var progressTotal = getPercent * getProgressWrapWidth;

        var animationLength = 2000;
        // on page load, animate percentage bar to data percentage length
        // .stop() used to prevent animation queueing
        selector.find('.custom__progress-bar').stop().animate({
            left: progressTotal
        }, animationLength);
    }

    // =================================================== progressbar ===================================================

    // =================================================== videoslider ===================================================


    (function ($, window, undefined) {
        'use strict';

        function throttle(func, delay) {
            var timer = null;

            return function () {
                var context = this,
                    args = arguments;

                if (timer === null) {
                    timer = setTimeout(function () {
                        func.apply(context, args);
                        timer = null;
                    }, delay);
                }
            };
        }

        // Check for browser CSS support and cache the result for subsequent calls.
        var checkStyleSupport = (function () {
            var support = {};
            return function (prop) {
                if (support[prop] !== undefined) {
                    return support[prop];
                }

                var div = document.createElement('div'),
                    style = div.style,
                    ucProp = prop.charAt(0).toUpperCase() + prop.slice(1),
                    prefixes = ["webkit", "moz", "ms", "o"],
                    props = (prop + ' ' + (prefixes).join(ucProp + ' ') + ucProp).split(' ');

                for (var i in props) {
                    if (props[i] in style) {
                        return support[prop] = props[i];
                    }
                }

                return support[prop] = false;
            };
        }());

        var svgNS = 'http://www.w3.org/2000/svg',
            svgSupport = (function () {
                var support;
                return function () {
                    if (support !== undefined) {
                        return support;
                    }
                    var div = document.createElement('div');
                    div.innerHTML = '<svg/>';
                    support = (div.firstChild && div.firstChild.namespaceURI === svgNS);
                    return support;
                };
            }());

        var $window = $(window),

            transformSupport = checkStyleSupport('transform'),

            defaults = {
                itemContainer: 'ul',
                // [string|object]
                // Selector for the container of the flippin' items.

                itemSelector: 'li',
                // [string|object]
                // Selector for children of `itemContainer` to flip

                start: 'center',
                // ['center'|number]
                // Zero based index of the starting item, or use 'center' to start in the middle

                fadeIn: 400,
                // [milliseconds]
                // Speed of the fade in animation after items have been setup

                loop: false,
                // [true|false|number]
                // Loop around when the start or end is reached
                // If number, this is the number of items that will be shown when the beginning or end is reached

                autoplay: false,
                // [false|milliseconds]
                // If a positive number, Flipster will automatically advance to next item after that number of milliseconds

                pauseOnHover: true,
                // [true|false]
                // If true, autoplay advancement will pause when Flipster is hovered

                style: 'coverflow',
                // [coverflow|carousel|flat|...]
                // Adds a class (e.g. flipster--coverflow) to the flipster element to switch between display styles
                // Create your own theme in CSS and use this setting to have Flipster add the custom class

                spacing: -0.6,
                // [number]
                // Space between items relative to each item's width. 0 for no spacing, negative values to overlap

                click: true,
                // [true|false]
                // Clicking an item switches to that item

                keyboard: true,
                // [true|false]
                // Enable left/right arrow navigation

                scrollwheel: true,
                // [true|false]
                // Enable mousewheel/trackpad navigation; up/left = previous, down/right = next

                touch: true,
                // [true|false]
                // Enable swipe navigation for touch devices

                nav: false,
                // [true|false|'before'|'after']
                // If not false, Flipster will build an unordered list of the items
                // Values true or 'before' will insert the navigation before the items, 'after' will append the navigation after the items

                buttons: false,
                // [true|false|'custom']
                // If true, Flipster will insert Previous / Next buttons with SVG arrows
                // If 'custom', Flipster will not insert the arrows and will instead use the values of `buttonPrev` and `buttonNext`

                buttonPrev: 'Previous',
                // [text|html]
                // Changes the text for the Previous button

                buttonNext: 'Next',
                // [text|html]
                // Changes the text for the Next button

                onItemSwitch: false
                // [function]
                // Callback function when items are switched
                // Arguments received: [currentItem, previousItem]
            },

            classes = {
                main: 'flipster',
                active: 'flipster--active',
                container: 'flipster__container',

                nav: 'flipster__nav',
                navChild: 'flipster__nav__child',
                navItem: 'flipster__nav__item',
                navLink: 'flipster__nav__link',
                navCurrent: 'flipster__nav__item--current',
                navCategory: 'flipster__nav__item--category',
                navCategoryLink: 'flipster__nav__link--category',

                button: 'flipster__button',
                buttonPrev: 'flipster__button--prev',
                buttonNext: 'flipster__button--next',

                item: 'flipster__item',
                itemCurrent: 'flipster__item--current',
                itemPast: 'flipster__item--past',
                itemFuture: 'flipster__item--future',
                itemContent: 'flipster__item__content'
            },

            classRemover = new RegExp('\\b(' + classes.itemCurrent + '|' + classes.itemPast + '|' + classes.itemFuture + ')(.*?)(\\s|$)', 'g'),
            whiteSpaceRemover = new RegExp('\\s\\s+', 'g');

        $.fn.flipster = function (options) {
            var isMethodCall = (typeof options === 'string' ? true : false);

            if (isMethodCall) {
                var args = Array.prototype.slice.call(arguments, 1);
                return this.each(function () {
                    var methods = $(this).data('methods');
                    if (methods[options]) {
                        return methods[options].apply(this, args);
                    } else {
                        return this;
                    }
                });
            }

            var settings = $.extend({}, defaults, options);

            return this.each(function () {

                var self = $(this),
                    methods,

                    _container,
                    _containerWidth,

                    _items,
                    _itemOffsets = [],
                    _currentItem,
                    _currentIndex = 0,

                    _nav,
                    _navItems,
                    _navLinks,

                    _playing = false,
                    _startDrag = false;

                function buildButtonContent(dir) {
                    var text = (dir === 'next' ? settings.buttonNext : settings.buttonPrev);

                    if (settings.buttons === 'custom' || !svgSupport) {
                        return text;
                    }

                    return '<svg viewBox="0 0 13 20" xmlns="' + svgNS + '" aria-labelledby="title"><title>' + text + '</title><polyline points="10,3 3,10 10,17"' + (dir === 'next' ? ' transform="rotate(180 6.5,10)"' : '') + '/></svg>';
                }

                function buildButton(dir) {
                    dir = dir || 'next';

                    return $('<button class="' + classes.button + ' ' + (dir === 'next' ? classes.buttonNext : classes.buttonPrev) + '" role="button" />')
                        .html(buildButtonContent(dir))
                        .on('click', function (e) {
                            jump(dir);
                            e.preventDefault();
                        });

                }

                function buildButtons() {
                    if (settings.buttons && _items.length > 1) {
                        self.find('.' + classes.button).remove();
                        self.append(buildButton('prev'), buildButton('next'));
                    }
                }

                function buildNav() {
                    var navCategories = {};

                    if (!settings.nav || _items.length <= 1) {
                        return;
                    }

                    if (_nav) {
                        _nav.remove();
                    }

                    _nav = $('<ul class="' + classes.nav + '" role="navigation" />');
                    _navLinks = $('');

                    _items.each(function (i) {
                        var item = $(this),
                            category = item.data('flip-category'),
                            itemTitle = item.data('flip-title') || item.attr('title') || i,
                            navLink = $('<a href="#" class="' + classes.navLink + '">' + itemTitle + '</a>')
                                .data('index', i);

                        _navLinks = _navLinks.add(navLink);

                        if (category) {

                            if (!navCategories[category]) {

                                var categoryItem = $('<li class="' + classes.navItem + ' ' + classes.navCategory + '">');
                                var categoryLink = $('<a href="#" class="' + classes.navLink + ' ' + classes.navCategoryLink + '" data-flip-category="' + category + '">' + category + '</a>')
                                    .data('category', category)
                                    .data('index', i);

                                navCategories[category] = $('<ul class="' + classes.navChild + '" />');

                                _navLinks = _navLinks.add(categoryLink);

                                categoryItem
                                    .append(categoryLink, navCategories[category])
                                    .appendTo(_nav);
                            }

                            navCategories[category].append(navLink);
                        } else {
                            _nav.append(navLink);
                        }

                        navLink.wrap('<li class="' + classes.navItem + '">');

                    });

                    _nav.on('click', 'a', function (e) {
                        var index = $(this).data('index');
                        if (index >= 0) {
                            jump(index);
                            e.preventDefault();
                        }
                    });

                    if (settings.nav === 'after') {
                        self.append(_nav);
                    }
                    else {
                        self.prepend(_nav);
                    }

                    _navItems = _nav.find('.' + classes.navItem);
                }

                function updateNav() {
                    if (settings.nav) {

                        var category = _currentItem.data('flip-category');

                        _navItems.removeClass(classes.navCurrent);

                        _navLinks
                            .filter(function () {
                                return ($(this).data('index') === _currentIndex || (category && $(this).data('category') === category));
                            })
                            .parent()
                            .addClass(classes.navCurrent);

                    }
                }

                function noTransition() {
                    self.css('transition', 'none');
                    _container.css('transition', 'none');
                    _items.css('transition', 'none');
                }

                function resetTransition() {
                    self.css('transition', '');
                    _container.css('transition', '');
                    _items.css('transition', '');
                }

                function calculateBiggestItemHeight() {
                    var biggestHeight = 0,
                        itemHeight;

                    _items.each(function () {
                        itemHeight = $(this).height();
                        if (itemHeight > biggestHeight) {
                            biggestHeight = itemHeight;
                        }
                    });
                    return biggestHeight;
                }

                function resize(skipTransition) {
                    if (skipTransition) {
                        noTransition();
                    }

                    _containerWidth = _container.width();
                    _container.height(calculateBiggestItemHeight());

                    _items.each(function (i) {
                        var item = $(this),
                            width,
                            left;

                        item.attr('class', function (i, c) {
                            return c && c.replace(classRemover, '').replace(whiteSpaceRemover, ' ');
                        });

                        width = item.outerWidth();

                        if (settings.spacing !== 0) {
                            item.css('margin-right', (width * settings.spacing) + 'px');
                        }

                        left = item.position().left;
                        _itemOffsets[i] = -1 * ((left + (width / 2)) - (_containerWidth / 2));

                        if (i === _items.length - 1) {
                            center();
                            if (skipTransition) {
                                setTimeout(resetTransition, 1);
                            }
                        }
                    });
                }

                function center() {
                    var total = _items.length,
                        loopCount = (settings.loop !== true && settings.loop > 0 ? settings.loop : false),
                        item, newClass, zIndex, past, offset;

                    if (_currentIndex >= 0) {

                        _items.each(function (i) {
                            item = $(this);
                            newClass = ' ';

                            if (i === _currentIndex) {
                                newClass += classes.itemCurrent;
                                zIndex = (total + 2);
                            } else {
                                past = (i < _currentIndex ? true : false);
                                offset = (past ? _currentIndex - i : i - _currentIndex);

                                if (loopCount) {
                                    if (_currentIndex <= loopCount && i > _currentIndex + loopCount) {
                                        past = true;
                                        offset = (total + _currentIndex) - i;
                                    } else if (_currentIndex >= total - loopCount && i < _currentIndex - loopCount) {
                                        past = false;
                                        offset = (total - _currentIndex) + i;
                                    }
                                }

                                newClass += (past ?
                                        classes.itemPast + ' ' + classes.itemPast + '-' + offset :
                                        classes.itemFuture + ' ' + classes.itemFuture + '-' + offset
                                );

                                zIndex = total - offset;
                            }

                            item
                                .css('z-index', zIndex * 2)
                                .attr('class', function (i, c) {
                                    return c && c.replace(classRemover, '').replace(whiteSpaceRemover, ' ') + newClass;
                                });
                        });

                        if (!_containerWidth || _itemOffsets[_currentIndex] === undefined) {
                            resize(true);
                        }

                        if (transformSupport) {
                            _container.css('transform', 'translateX(' + _itemOffsets[_currentIndex] + 'px)');
                        } else {
                            _container.css('left', _itemOffsets[_currentIndex] + 'px');
                        }
                    }

                    updateNav();
                }

                function jump(to) {
                    var _previous = _currentIndex;

                    if (_items.length <= 1) {
                        return;
                    }

                    if (to === 'prev') {
                        if (_currentIndex > 0) {
                            _currentIndex--;
                        }
                        else if (settings.loop) {
                            _currentIndex = _items.length - 1;
                        }
                    } else if (to === 'next') {
                        if (_currentIndex < _items.length - 1) {
                            _currentIndex++;
                        }
                        else if (settings.loop) {
                            _currentIndex = 0;
                        }
                    } else if (typeof to === 'number') {
                        _currentIndex = to;
                    } else if (to !== undefined) {
                        // if object is sent, get its index
                        _currentIndex = _items.index(to);
                    }

                    _currentItem = _items.eq(_currentIndex);

                    if (_currentIndex !== _previous && settings.onItemSwitch) {
                        settings.onItemSwitch.call(self, _items[_currentIndex], _items[_previous]);
                    }

                    center();

                    return self;
                }

                function play(interval) {
                    settings.autoplay = interval || settings.autoplay;

                    clearInterval(_playing);

                    _playing = setInterval(function () {
                        var prev = _currentIndex;
                        jump('next');
                        if (prev === _currentIndex && !settings.loop) {
                            clearInterval(_playing);
                        }
                    }, settings.autoplay);

                    return self;
                }

                function pause() {
                    clearInterval(_playing);
                    if (settings.autoplay) {
                        _playing = -1;
                    }

                    return self;
                }

                function show() {
                    resize(true);
                    self.hide()
                        .css('visibility', '')
                        .addClass(classes.active)
                        .fadeIn(settings.fadeIn);
                }

                function index() {

                    _container = self.find(settings.itemContainer).addClass(classes.container);

                    _items = _container.find(settings.itemSelector);

                    if (_items.length <= 1) {
                        return;
                    }

                    _items
                        .addClass(classes.item)
                        // Wrap inner content
                        .each(function () {
                            var item = $(this);
                            if (!item.children('.' + classes.itemContent).length) {
                                item.wrapInner('<div class="' + classes.itemContent + '" />');
                            }
                        });

                    // Navigate directly to an item by clicking
                    if (settings.click) {
                        _items.on('click.flipster touchend.flipster', function (e) {
                            if (!_startDrag) {
                                if (!$(this).hasClass(classes.itemCurrent)) {
                                    e.preventDefault();
                                }
                                jump(this);
                            }
                        });
                    }

                    // Insert navigation if enabled.
                    buildButtons();
                    buildNav();

                    if (_currentIndex >= 0) {
                        jump(_currentIndex);
                    }

                    return self;
                }

                function keyboardEvents(elem) {
                    if (settings.keyboard) {
                        elem[0].tabIndex = 0;
                        elem.on('keydown.flipster', throttle(function (e) {
                            var code = e.which;
                            if (code === 37 || code === 39) {
                                jump(code === 37 ? 'prev' : 'next');
                                e.preventDefault();
                            }
                        }, 250, true));
                    }
                }

                function wheelEvents(elem) {
                    if (settings.scrollwheel) {
                        var _wheelInside = false,
                            _actionThrottle = 0,
                            _throttleTimeout = 0,
                            _delta = 0,
                            _dir, _lastDir;

                        elem
                            .on('mousewheel.flipster wheel.flipster', function () {
                                _wheelInside = true;
                            })
                            .on('mousewheel.flipster wheel.flipster', throttle(function (e) {

                                // Reset after a period without scrolling.
                                clearTimeout(_throttleTimeout);
                                _throttleTimeout = setTimeout(function () {
                                    _actionThrottle = 0;
                                    _delta = 0;
                                }, 300);

                                e = e.originalEvent;

                                // Add to delta (+=) so that continuous small events can still get past the speed limit, and quick direction reversals get cancelled out
                                _delta += (e.wheelDelta || (e.deltaY + e.deltaX) * -1); // Invert numbers for Firefox

                                // Don't trigger unless the scroll is decent speed.
                                if (Math.abs(_delta) < 25) {
                                    return;
                                }

                                _actionThrottle++;

                                _dir = (_delta > 0 ? 'prev' : 'next');

                                // Reset throttle if direction changed.
                                if (_lastDir !== _dir) {
                                    _actionThrottle = 0;
                                }
                                _lastDir = _dir;

                                // Regular scroll wheels trigger less events, so they don't need to be throttled. Trackpads trigger many events (inertia), so only trigger jump every three times to slow things down.
                                if (_actionThrottle < 6 || _actionThrottle % 3 === 0) {
                                    jump(_dir);
                                }

                                _delta = 0;

                            }, 50));

                        // Disable mousewheel on window if event began in elem.
                        $window.on('mousewheel.flipster wheel.flipster', function (e) {
                            if (_wheelInside) {
                                e.preventDefault();
                                _wheelInside = false;
                            }
                        });
                    }
                }

                function touchEvents(elem) {
                    if (settings.touch) {
                        var _startDragY = false,
                            _touchJump = throttle(jump, 300),
                            x, y, offsetY, offsetX;

                        elem.on({
                            'touchstart.flipster': function (e) {
                                e = e.originalEvent;
                                _startDrag = (e.touches ? e.touches[0].clientX : e.clientX);
                                _startDragY = (e.touches ? e.touches[0].clientY : e.clientY);
                                //e.preventDefault();
                            },

                            'touchmove.flipster': throttle(function (e) {
                                if (_startDrag !== false) {
                                    e = e.originalEvent;

                                    x = (e.touches ? e.touches[0].clientX : e.clientX);
                                    y = (e.touches ? e.touches[0].clientY : e.clientY);
                                    offsetY = y - _startDragY;
                                    offsetX = x - _startDrag;

                                    if (Math.abs(offsetY) < 100 && Math.abs(offsetX) >= 30) {
                                        _touchJump((offsetX < 0 ? 'next' : 'prev'));
                                        _startDrag = x;
                                        e.preventDefault();
                                    }

                                }
                            }, 100),

                            'touchend.flipster touchcancel.flipster ': function () {
                                _startDrag = false;
                            }
                        });
                    }
                }

                function init() {

                    var style;

                    self.css('visibility', 'hidden');

                    index();

                    if (_items.length <= 1) {
                        self.css('visibility', '');
                        return;
                    }

                    style = (settings.style ? 'flipster--' + settings.style.split(' ').join(' flipster--') : false);

                    self.addClass([
                        classes.main,
                        (transformSupport ? 'flipster--transform' : ' flipster--no-transform'),
                        style, // 'flipster--'+settings.style : '' ),
                        (settings.click ? 'flipster--click' : '')
                    ].join(' '));

                    // Set the starting item
                    if (settings.start) {
                        // Find the middle item if start = center
                        _currentIndex = (settings.start === 'center' ? Math.floor(_items.length / 2) : settings.start);
                    }

                    jump(_currentIndex);

                    var images = self.find('img');

                    if (images.length) {
                        var imagesLoaded = 0;

                        // Resize after all images have loaded.
                        images.on('load', function () {
                            imagesLoaded++;
                            if (imagesLoaded >= images.length) {
                                show();
                            }
                        });

                        // Fallback to show Flipster while images load in case it takes a while.
                        setTimeout(show, 750);
                    } else {
                        show();
                    }

                    // Attach event bindings.
                    $window.on('resize.flipster', throttle(resize, 400));

                    if (settings.autoplay) {
                        play();
                    }

                    if (settings.pauseOnHover) {
                        _container
                            .on('mouseenter.flipster', pause)
                            .on('mouseleave.flipster', function () {
                                if (_playing === -1) {
                                    play();
                                }
                            });
                    }

                    keyboardEvents(self);
                    wheelEvents(_container);
                    touchEvents(_container);
                }

                // public methods
                methods = {
                    jump: jump,
                    next: function () {
                        return jump('next');
                    },
                    prev: function () {
                        return jump('prev');
                    },
                    play: play,
                    pause: pause,
                    index: index
                };
                self.data('methods', methods);

                // Initialize if flipster is not already active.
                if (!self.hasClass(classes.active)) {
                    init();
                }
            });
        };
    })(jQuery, window);


    var flipContainer = $('.flipster'),
        flipItemContainer = flipContainer.find('.flip-items'),
        flipItem = flipContainer.find('li');

    // flipContainer.flipster({
    //     itemContainer: flipItemContainer,
    //     itemSelector: flipItem,
    //     loop: 1,
    //     start: 2,
    //     style: 'infinite-carousel',
    //     spacing: 0,
    //     scrollwheel: false,
    //     //nav: 'after',
    //     buttons: true
    // });

    flipContainer.flipster({
        itemContainer: flipItemContainer,
        itemSelector: flipItem,
        loop: 1,
        start: 2,
        style: 'infinite-carousel',
        spacing: 0,
        scrollwheel: false,
        //nav: 'after',
        buttons: true
    });
    // =================================================== videoslider ===================================================


    // =================================================== owl carousel ===================================================


    // tabs + owl and tabs + reps

    // $('.tab-content > .tab-pane.fade').each(function () {
    //
    //     if ($(this).hasClass('active')) {
    //         $(this).addClass('firstt');
    //         $(this).closest('.tab-content').find('.tab-pane').addClass('active');
    //         $('.clubs__slider').owlCarousel({
    //             items: 1,
    //             nav: true,
    //             margin: 0,
    //             navText: ["<img src='../img/ar2.png'>", "<img src='../img/ar.png'>"],
    //             dots: false
    //         });
    //         $(this).closest('.tab-content').find('.tab-pane').removeClass('active');
    //         $(this).closest('.tab-content').find('.tab-pane.firstt').addClass('active in');
    //     }
    // });


// tabs resp end

    $('.stages__slider').owlCarousel({
        items: 5,
        nav: true,
        navText: ["<img src='../img/ar2.png'>", "<img src='../img/ar.png'>"],
        dots: false,
        responsive: {
            320: {
                items: 1
            },
            500: {
                items: 2
            },
            769: {
                items: 2
            },
            993: {
                items: 3
            },
            1201: {
                items: 4
            }
        }
    });


    $('.localisation__slider').owlCarousel({
        items: 1,
        nav: true,
        navText: ["<div class='arl'></div>", "<div class='arr'></div>"],
        dots: false,
        margin: 0,
        loop: true,
        responsive: {
            320: {
                items: 1
            },
            500: {
                items: 1
            },
            769: {
                items: 1
            },
            1200: {
                items: 1
            }
        }
    });


    $('.news__slider').owlCarousel({
        items: 3,
        // nav: true,
        // arrows: false,
        margin: 0,
        dotsEach: true,
        dots: true,
        responsive: {
            320: {
                items: 1
            },
            769: {
                items: 2
            },
            1200: {
                items: 3
            }
        }
    });


    // =================================================== owl carousel ===================================================


    // =================================================== team logic ===================================================

    var human = $('.team__player').not('.disabled');

    var humanSingle = $('.team__big');


    for (var i = 0; i < humanSingle.length; i++) {
        $(humanSingle[i]).attr('data-id', i);
    }

    for (var i = 0; i < human.length; i++) {
        $(human[i]).attr('data-id', i);

        if ($(human[i]).hasClass('active')) {
            $('.team__big[data-id="' + $(human[i]).data('id') + '"]').css('display', 'block');
        }
    }

    $(document).on('click', '.team__player', function (e) {

        var index = $(this).data('id');

        humanSingle.css('display', 'none');

        setTimeout(function () {
            humanSingle.removeClass('active');
        }, 100);

        human.removeClass('active');

        $('.team__big[data-id="' + index + '"]').css('display', 'block');

        setTimeout(function () {
            $('.team__big[data-id="' + index + '"]').addClass('active');
        }, 100);


        $('.team__player[data-id="' + index + '"]').addClass('active');

        if ($(window).width() < 769) {

            $('body,html').stop().animate(
                {'scrollTop': $('.team').offset().top - $('header').outerHeight()},
                400
            );
            500
        }
    });

    function callback(event) {

        human.removeClass('active');
        humanSingle.css('display', 'none');

        var item = $('.owl-item.active').find('.team__player');

        item.first().addClass('active');

        $('.team__big[data-id="' + item.data('id') + '"]').css('display', 'block');


    }

    $('.team__slider').owlCarousel({
        items: 1,
        nav: true,
        arrows: true,
        margin: 0,
        dotsEach: true,
        dots: true,
        navText: ["<div class='arl'></div>", "<div class='arr'></div>"],
        onTranslated: callback,
        mouseDrag: false,

        responsive: {
            320: {
                items: 1
            },
            769: {
                items: 1
            },
            1200: {
                items: 1
            }
        }
    });

    if ($(window).width() < 769) {

        $('.team__big__wrapper').addClass('owl-theme owl-carousel team__big__wrapper-slider');

        humanSingle.css('display', 'block');

        $('.team__big__wrapper-slider').owlCarousel({
            items: 1,
            nav: true,
            arrows: true,
            margin: 0,
            dotsEach: true,
            dots: false,
            navText: ["<div class='arl'></div>", "<div class='arr'></div>"],
            mouseDrag: true,
            responsive: {
                320: {
                    items: 1
                },
                769: {
                    items: 1
                },
                1200: {
                    items: 1
                }
            }
        });


    }


    // =================================================== team logic ===================================================


    // =================================================== dropdown logic ===================================================

    $('.faq__item').on('click', function () {
        // alert('najal');
        $('.faq__item').not($(this)).removeClass('active');

        if (!$(this).hasClass('active')) {
            $(this).addClass('active');
        } else {
            $(this).removeClass('active');
        }

    });

    // =================================================== dropdown logic ===================================================


    // =================================================== form ===================================================


    function removePopup() {

        $('.mail-popup__wrapper').hide(300).removeClass('visible error success');
        $('.mail-popup__error').hide(300);
        $('.mail-popup__success').hide(300);

    }

    // $(document).on('submit', '.mail__form form', function (e) {
    //
    //     e.preventDefault();
    //
    //     var url = $(this).data('url');
    //
    //     var value = $(this).closest('form').find('input').val();
    //
    //     var pattern = new RegExp('[a-z0-9._%+-]+@[a-z0-9.-]+\\.[a-z]{2,3}$');
    //
    //     if (pattern.test(value)) {
    //         $.ajax({
    //             url: url,
    //             method: 'GET',
    //             dataType: 'html',
    //             async: false,
    //             success: function (result) {
    //                 $('.mail-popup__wrapper').css('display', 'flex').addClass('visible success');
    //                 $('.mail-popup').show(300);
    //                 $('.mail-popup__success').show(300);
    //                 console.log(this);
    //                 e.prevent
    //             },
    //             error: function (result) {
    //                 $('.mail-popup__wrapper').css('display', 'flex').addClass('visible error');
    //                 $('.mail-popup').show(300);
    //                 $('.mail-popup__error').show(300);
    //             }
    //         });
    //     } else {
    //         $('.mail-popup__wrapper').css('display', 'flex').addClass('visible error');
    //         $('.mail-popup').show(300);
    //         $('.mail-popup__error').show(300);
    //     }
    //
    //     setTimeout(removePopup, 3000);
    //
    //
    // });


    // =================================================== form ===================================================


    // =================================================== header ===================================================


    function stickyHead() {
        if ($(window).scrollTop() > 1) {
            $('header').addClass('active');
        } else {
            $('header').removeClass('active');
        }
    }

    stickyHead();

    $(window).scroll(function () {
        stickyHead();
    });


    $('.first-block').css('padding-top', $('header').outerHeight());

    // =================================================== header ===================================================


    // =================================================== svg fill ===================================================
    jQuery('img.svg').each(function () {
        var $img = jQuery(this);
        var imgID = $img.attr('id');
        var imgClass = $img.attr('class');
        var imgURL = $img.attr('src');

        jQuery.get(imgURL, function (data) {
            // Get the SVG tag, ignore the rest
            var $svg = jQuery(data).find('svg');

            // Add replaced image's ID to the new SVG
            if (typeof imgID !== 'undefined') {
                $svg = $svg.attr('id', imgID);
            }
            // Add replaced image's classes to the new SVG
            if (typeof imgClass !== 'undefined') {
                $svg = $svg.attr('class', imgClass + ' replaced-svg');
            }

            // Remove any invalid XML tags as per http://validator.w3.org
            $svg = $svg.removeAttr('xmlns:a');

            // Check if the viewport is set, if the viewport is not set the SVG wont't scale.
            if (!$svg.attr('viewBox') && $svg.attr('height') && $svg.attr('width')) {
                $svg.attr('viewBox', '0 0 ' + $svg.attr('height') + ' ' + $svg.attr('width'))
            }

            // Replace image with new SVG
            $img.replaceWith($svg);

        }, 'xml');

    });
    // ===================================================  product item click @watch@ ===================================================


    $('.product__item .button-invite').on('click', function (e) {

        e.preventDefault();


        $('.product__item').not($(this).closest('.product__item')).removeClass('active').addClass('invisible-block');

        if (!$(this).closest('.product__item').hasClass('active')) {
            $(this).closest('.product__item').removeClass('invisible-block');
            $(this).closest('.product__item').addClass('active');
        } else {
            $(this).closest('.product__item').removeClass('active');
            $('.product__item').removeClass('invisible-block');
        }


    });

    // =================================================== product item click @watch@ ===================================================


    // =================================================== whitelist ===================================================

    $('.whitelist').on('click', function (e) {

        e.preventDefault();
        $('body').addClass('modal-open');
        $('.whitelist__form__wrapper').addClass('active');

    });


    $('.whitelist__cross').on('click', function (e) {

        e.preventDefault();

        $('body').removeClass('modal-open');
        $('.whitelist__form__wrapper').removeClass('active');

    });


    // =================================================== whitelist ===================================================

    // =================================================== tabs first item ===================================================


    // $('.custom-tab__link').on('click', function (e) {
    //     var columnHash = $(this).attr('href');
    //     columnHash = columnHash.replace('#','');
    //     console.log(columnHash);
    //     $(this).closest('.team__list').find('.team__item').removeClass('active');
    //     $(this).closest('.team__wrapper').find('.team__human').removeClass('active').css('display','none');
    //
    //     var activeItemMini = $(this).closest('.team__list').find('.tab-pane#' + columnHash + ' ').find('.team__item').first();
    //
    //     var activeIndex = activeItemMini.data('id');
    //
    //     activeItemMini.addClass('active');
    //
    //     $(this).closest('.team__wrapper').find('.team__human[data-id="'+activeIndex+'"]').addClass('active').css('display','block');
    // });


    // =================================================== tabs first item ===================================================

    //


    // =================================================== animate css ===================================================

    var wow = new WOW(
        {
            boxClass: 'wow',      // animated element css class (default is wow)
            animateClass: 'animated', // animation css class (default is animated)
            offset: 0,          // distance to the element when triggering the animation (default is 0)
            mobile: true,       // trigger animations on mobile devices (default is true)
            live: true,       // act on asynchronously loaded content (default is true)
            callback: function (box) {
                // the callback is fired every time an animation is started
                // the argument that is passed in is the DOM node being animated
            }
        }
    );


    if ($(window).width() > 768) {
        wow.init();

    }
    // =================================================== animate css ===================================================


    // =============================     // position of our team items ===================================================


    function setPlayersCoordinates(playersPosition) {

        $('.team__player[data-id="0"]').css({
            top: parseInt(playersPosition.attackCenter.top),
            left: parseInt(playersPosition.attackCenter.left)
        });

        $('.team__player[data-id="1"]').css({
            top: parseInt(playersPosition.attackTop.top),
            left: parseInt(playersPosition.attackTop.left)
        });

        $('.team__player[data-id="2"]').css({
            top: parseInt(playersPosition.attackBottom.top),
            left: parseInt(playersPosition.attackBottom.left)
        });

        $('.team__player[data-id="3"]').css({
            top: parseInt(playersPosition.middleTop.top),
            left: parseInt(playersPosition.middleTop.left)
        });

        $('.team__player[data-id="4"]').css({
            top: parseInt(playersPosition.middleCenter.top),
            left: parseInt(playersPosition.middleCenter.left)
        });

        $('.team__player[data-id="5"]').css({
            top: parseInt(playersPosition.middleBottom.top),
            left: parseInt(playersPosition.middleBottom.left)
        });

        $('.team__player[data-id="6"]').css({
            top: parseInt(playersPosition.backTop.top),
            left: parseInt(playersPosition.backTop.left)
        });

        $('.team__player[data-id="7"]').css({
            top: parseInt(playersPosition.backFrontCenter.top),
            left: parseInt(playersPosition.backFrontCenter.left)
        });

        $('.team__player[data-id="8"]').css({
            top: parseInt(playersPosition.backBackCenter.top),
            left: parseInt(playersPosition.backBackCenter.left)
        });

        $('.team__player[data-id="9"]').css({
            top: parseInt(playersPosition.backBottom.top),
            left: parseInt(playersPosition.backBottom.left)
        });

        $('.team__player[data-id="10"]').css({
            top: parseInt(playersPosition.goalKeeper.top),
            left: parseInt(playersPosition.goalKeeper.left)
        });

        $('.team__player[data-id="11"]').css({
            top: parseInt(playersPosition.attackCenter.top),
            left: parseInt(playersPosition.attackCenter.left)
        });

        $('.team__player[data-id="12"]').css({
            top: parseInt(playersPosition.middleCenter.top),
            left: parseInt(playersPosition.middleCenter.left)
        });

        $('.team__player[data-id="13"]').css({
            top: parseInt(playersPosition.attackExtra.top),
            left: parseInt(playersPosition.attackExtra.left)
        });

        $('.team__player[data-id="14"]').css({
            top: parseInt(playersPosition.goalKeeper.top),
            left: parseInt(playersPosition.goalKeeper.left)
        });
    }


    function getFieldCoordinates() {

        var fieldCoords = {};

        var attackBlock = $('#XMLID_27_');
        var middleBlock = $('#XMLID_28_');
        var backBlock = $('#XMLID_29_');
        var goalKeeperBlock = $('#XMLID_30_');

        // console.log(attackBlock[0].getBoundingClientRect().top, attackBlock.closest('.team__slide__field').offset().top);

        if (/^((?!chrome|android).)*safari/i.test(navigator.userAgent)) {

            fieldCoords.attackLine = {
                top: attackBlock[0].getBoundingClientRect().top - attackBlock.closest('.team__slide__field').offset().top,
                left: attackBlock[0].getBoundingClientRect().left - attackBlock.closest('.team__slide__field').offset().left
            };

            fieldCoords.middleLine = {
                top: middleBlock[0].getBoundingClientRect().top - middleBlock.closest('.team__slide__field').offset().top,
                left: middleBlock[0].getBoundingClientRect().left - middleBlock.closest('.team__slide__field').offset().left
            };

            fieldCoords.backLine = {
                top: backBlock[0].getBoundingClientRect().top - backBlock.closest('.team__slide__field').offset().top,
                left: backBlock[0].getBoundingClientRect().left - backBlock.closest('.team__slide__field').offset().left
            };

            fieldCoords.goalKeeperLine = {
                top: goalKeeperBlock[0].getBoundingClientRect().top - goalKeeperBlock.closest('.team__slide__field').offset().top,
                left: goalKeeperBlock[0].getBoundingClientRect().left - goalKeeperBlock.closest('.team__slide__field').offset().left
            };

        } else {

            fieldCoords.attackLine = {
                top: attackBlock.offset().top - attackBlock.closest('.team__slide__field').offset().top,
                left: attackBlock.offset().left - attackBlock.closest('.team__slide__field').offset().left
            };

            fieldCoords.middleLine = {
                top: middleBlock.offset().top - middleBlock.closest('.team__slide__field').offset().top,
                left: middleBlock.offset().left - middleBlock.closest('.team__slide__field').offset().left
            };

            fieldCoords.backLine = {
                top: backBlock.offset().top - backBlock.closest('.team__slide__field').offset().top,
                left: backBlock.offset().left - backBlock.closest('.team__slide__field').offset().left
            };

            fieldCoords.goalKeeperLine = {
                top: goalKeeperBlock.offset().top - goalKeeperBlock.closest('.team__slide__field').offset().top,
                left: goalKeeperBlock.offset().left - goalKeeperBlock.closest('.team__slide__field').offset().left
            };

        }
        var tshirtGabarites = {
            height: $('.team__player').css('height'),
            width: $('.team__player').css('width')
        };

        var playersPosition = {
            attackTop: {
                top: parseInt(fieldCoords.attackLine.top) + parseInt(tshirtGabarites.height) * 1.2,
                left: parseInt(fieldCoords.attackLine.left)
            },
            attackExtra: {
                top: parseInt(fieldCoords.attackLine.top) + parseInt(tshirtGabarites.height) * 1.3,
                left: parseInt(fieldCoords.attackLine.left) - parseInt(tshirtGabarites.width)
            },
            attackCenter: {
                top: parseInt(fieldCoords.attackLine.top) + parseInt(tshirtGabarites.height) * 2,
                left: parseInt(fieldCoords.attackLine.left) + parseInt(tshirtGabarites.width)
            },
            attackBottom: {
                top: parseInt(fieldCoords.attackLine.top) + parseInt(tshirtGabarites.height) * 3.2,
                left: parseInt(fieldCoords.attackLine.left) + parseInt(tshirtGabarites.width) / 3
            },
            middleTop: {
                top: parseInt(fieldCoords.middleLine.top) + parseInt(tshirtGabarites.height) * 1.2,
                left: parseInt(fieldCoords.middleLine.left) + parseInt(tshirtGabarites.width)
            },
            middleCenter: {
                top: parseInt(fieldCoords.middleLine.top) + parseInt(tshirtGabarites.height) * 2,
                left: parseInt(fieldCoords.middleLine.left)
            },
            middleBottom: {
                top: parseInt(fieldCoords.middleLine.top) + parseInt(tshirtGabarites.height) * 3.2,
                left: parseInt(fieldCoords.middleLine.left) + parseInt(tshirtGabarites.width)
            }
            ,
            backTop: {
                top: parseInt(fieldCoords.backLine.top) + parseInt(tshirtGabarites.height) * 1.2,
                left: parseInt(fieldCoords.backLine.left) + parseInt(tshirtGabarites.width) / 2
            },
            backFrontCenter: {
                top: parseInt(fieldCoords.backLine.top) + parseInt(tshirtGabarites.height) * 2,
                left: parseInt(fieldCoords.backLine.left) + parseInt(tshirtGabarites.width) * 1.5
            },
            backBackCenter: {
                top: parseInt(fieldCoords.backLine.top) + parseInt(tshirtGabarites.height) * 2,
                left: parseInt(fieldCoords.backLine.left) - parseInt(tshirtGabarites.width) / 2
            },
            backBottom: {
                top: parseInt(fieldCoords.backLine.top) + parseInt(tshirtGabarites.height) * 3.2,
                left: parseInt(fieldCoords.backLine.left)
            },
            goalKeeper: {
                top: parseInt(fieldCoords.goalKeeperLine.top) + parseInt(tshirtGabarites.height) * 2,
                left: parseInt(fieldCoords.goalKeeperLine.left) + parseInt(tshirtGabarites.width)
            }
        };

        setPlayersCoordinates(playersPosition);


    }

    getFieldCoordinates();

    //


    $( window ).on( "orientationchange", function( event ) {
            getFieldCoordinates();
    });




    // =============================     // position of our team items ===================================================




});

