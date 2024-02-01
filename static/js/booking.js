"use strict";

/** Runs on listing/id page render.
 *
 * Calls api to check if listing is booked.
 *
 * If api return is true {booked: true}, hides 'book' and shows 'cancel' button
 * If api returns false {booked: false}, hides 'cancel' and shows 'book' button
 */
$(async function () {
  $("#book").on("click", book);
  $("#cancel").on("click", cancel);

  const urlParams = new URLSearchParams({ listing_id: listingId })
  const response = await fetch(`/api/bookings?${urlParams}`);
  const result = await response.json();

  if ("error" in result) {
    console.log(result.error);
  } else {
    let booked = result.booked;
    if (booked) $("#cancel").show();
    else $("#book").show();
  }
});

async function book(evt) {
  evt.preventDefault();

  let response = await fetch("/api/book",
    {
      method:"POST",
      body:JSON.stringify({ listing_id: listingId })
    });

  let result = response.data;

  if ("error" in result) {
    console.log(result.error);
  } else {
    $("#book").hide();
    $("#cancel").show();
  }
}

async function cancel(evt) {
  evt.preventDefault();

  let response = await fetch("/api/cancel",
  {
    method:"POST",
    body:JSON.stringify({ listing_id: listingId })
  });
  let result = response.data;

  if ("error" in result) {
    console.log(result.error);
  } else {
    $("#cancel").hide();
    $("#book").show();
  }
}